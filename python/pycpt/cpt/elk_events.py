import json
import logging
import os
from pathlib import Path
from typing import List

import requests

from cpt.configuration import setup_logging, fullname

ELK_URL_FROM_OS = os.getenv('ELK_BASE_URL') if os.getenv('ELK_BASE_URL') else "http://log01a.do.prg-krl.atc:5050"
ELK_BASE_URL = ELK_URL_FROM_OS if ELK_URL_FROM_OS.endswith("/") else ELK_URL_FROM_OS + '/'


class EventsSender:
    def __init__(self, events_file: Path):
        self.logger = setup_logging(fullname(self), level=logging.INFO)
        self.events_file = events_file
        self.events: List[dict] = []
        self.sent_events: List[dict] = []
        self.unsent_events: List[dict] = []
        self.load_events()

    def load_events(self):
        self.logger.info(f"Reading events : {self.events_file}")
        with open(self.events_file) as f:
            self.events = json.loads(f.read())

    def event_stats(self, field: str, value: str):
        """
        consistency check : during GQL extraction `gql_counts.json` gives
        expected count of executed calls for given GQL. The failed + passed
        must agree
        """
        passed = [e for e in self.events if e['event']['result'] == 'pass']
        failed = [e for e in self.events if e['event']['result'] == 'fail']
        passed_hash = [e['event'] for e in passed if e['event']['args'][field] == value]
        failed_hash: List[dict] = [e['event'] for e in failed if e['event']['args'][field] == value]
        self.logger.info(f"total {len(self.events)}, passed:{len(passed)} failed:{len(failed)}")
        self.logger.info(f"{value} : n_passed:{len(passed_hash)} n_failed:{len(failed_hash)}")
        m = 0
        for fail_hash in failed_hash:
            m += 1
            self.logger.debug(f"{m}.{fail_hash['error']['message']}")

    def post_events(self):
        length = len(self.events)
        self.logger.info(f"Post {length} to {ELK_BASE_URL}")
        for elk_event in self.events:
            self.post_event(elk_event)
            n_sent = len(self.sent_events)
            if n_sent % 100 == 0:
                print(f'sent ratio:{n_sent}/{length}')
                self.logger.info(f"{n_sent} sent events")

    def post_event(self, event: dict):
        event_type = event['eventType']
        elk_url = ELK_BASE_URL + event_type
        event_timestamp = event['timestamp']
        response = None
        try:
            response = requests.post(elk_url, verify=False, json=event, timeout=10)  # in seconds
        except requests.exceptions.RequestException as e:
            self.logger.info(f"response:{response}. Event {event} appended to unsent_events ")
            self.unsent_events.append(event)
            self.logger.error(e)
            print(e)
        if response and response.status_code == 200:
            self.sent_events.append(event)
        # response is not None so the event was not appended in except block
        elif response and response.status_code != 200:
            self.logger.info(f"response:{response}. Event {event} appended to unsent_events ")
            self.unsent_events.append(event)
            message = f"status code:{response.status_code}, timestamp:{event_timestamp}, event type:{event_type}"
            self.logger.error(message)
        # response is None and the reason of failure is not covered
        else:
            self.logger.error(f"Unknown reason for failure. response:{response}. "
                              f"Event {event} appended to unsent_events")
            self.unsent_events.append(event)

    def save_unsent_events(self):
        """ successfully sent event is removed from self.events """
        f_path, f_name = os.path.split(self.events_file)
        path = Path(f_path, "unsent_events.json")
        n_sent_events = len(self.sent_events)
        n_all_events = len(self.events)
        n_unsent_events = len(self.unsent_events)
        if n_all_events != n_sent_events:
            self.logger.info(f"sent events={n_sent_events} != all events {n_all_events}")
            with open(path, "w") as json_file:
                self.logger.info(f"Saving {n_unsent_events} usent events to {path}")
                json.dump(self.unsent_events, json_file, indent=4, sort_keys=True)
