import sys
from pathlib import Path

from cpt.elk_events import EventsSender

if __name__ == '__main__':
    file = Path(sys.argv[1])
    if file.exists():
        print(f"events from {file}")
        es = EventsSender(events_file=file)
        # logs these stats to cpt.log - just example
        es.event_stats(field="operationName", value="TermAggregation")
        es.event_stats(field="gqlHashMD5", value="e9a1aa519ec0240e17698e19f062dc3d")
        es.post_events()
        es.save_unsent_events()
    else:
        print(f"File does not exist {file}")
