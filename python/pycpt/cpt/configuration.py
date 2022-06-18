import logging
import os
import re
from configparser import RawConfigParser
from pathlib import Path
from typing import List

import typer


def log_file(log_file_name: str = "config.log"):
    try:
        r_v = os.getenv('LOG_DIR')
        l_f = r_v + log_file_name if r_v.endswith('/') else r_v + '/' + log_file_name
        return l_f
    except KeyError as k_e:
        l_f = Path(os.getcwd(), log_file_name)
        return l_f


def file_name_logger(file_name: str = 'cpt', folder: str = 'log'):
    logger = setup_logging(logger_name=file_name, level=logging.INFO, folder=folder, filename=f"{file_name}.log")
    log_path = Path(f"{os.getcwd()}", folder, f"{file_name}.log").resolve()
    return logger, log_path


def setup_logging(logger_name: str, folder: str = None, filename: str = "cpt.log", level: int = logging.INFO):
    if folder:
        os.makedirs(folder, exist_ok=True)
        filename = Path(folder, filename).resolve()
    logging.basicConfig(filename=filename, level=level,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(logger_name)
    return logger


def fullname(o):
    klass = o.__class__
    module = klass.__module__
    if module == 'builtins':
        return klass.__qualname__  # avoid outputs like 'builtins.str'
    return module + '.' + klass.__qualname__


class Logger:
    def __init__(self):
        self.logger = setup_logging(fullname(self))


class Configuration:
    SECTION = 'Main'
    TEST_ENV_KEY = "test_env"
    PROPERTY_PLACEHOLDER_RE = r"\${([\w\.-]+)}"

    def __init__(self, test_env: str,
                 resources: Path = Path('modules', 'api-tests', 'resources').resolve()):
        self.resources = resources
        self.test_env = test_env
        self.raw_properties: dict = {}
        self.properties: dict = {self.TEST_ENV_KEY: test_env}
        self.logger = setup_logging(fullname(self))
        self.load_properties()

    def load_properties(self):
        self.set_raw_properties()
        self.set_properties()

    def get_env_resources(self):
        self.logger.info(f"resources : {self.resources}")
        meta_properties_file = Path(self.resources, self.test_env + '.properties')
        if not meta_properties_file.exists():
            m = f"Meta properties file '{meta_properties_file}' does not exist! Exit"
            self.logger.error(m)
            # typer has more reliable echo that print for git bash
            typer.echo(m)
            exit(1)
        config = RawConfigParser()
        config.read(meta_properties_file)
        config_section = config.get(self.SECTION, 'env.resources') if config.has_section(self.SECTION) else None
        if not config_section:
            m = f"property file ={meta_properties_file} does not have section {self.SECTION}. Exit"
            self.logger.error(m)
            typer.echo(m)
            exit(2)
        return config_section

    def set_raw_properties(self):
        pf: List[str] = self.get_env_resources().split(';')
        for p_path in pf:
            # p_path contains 'resources/' again
            dir_name = p_path[p_path.index('/') + 1:]
            p_file = Path(self.resources, dir_name, 'test.properties')
            self.logger.info("reading %s", p_file.resolve())
            config = RawConfigParser()
            config.read(p_file)
            if config.has_section(self.SECTION):
                props = config.items(self.SECTION)
                for prop in props:
                    k = prop[0]
                    v = prop[1]
                    if k in self.raw_properties and self.raw_properties[k] == v:
                        self.logger.warning("duplicated key/value pair %s:%s", k, v)
                    self.raw_properties[k] = v
            else:
                raise Exception('Section {0} not found in the {1} file'.format(self.SECTION, p_file))

    def _interpolate(self, ret):
        prop_placeholders = re.findall(self.PROPERTY_PLACEHOLDER_RE, ret)
        for pp in prop_placeholders:
            self.logger.debug("resolving placeholder %s", pp)
            v = self.raw_properties[pp]
            v = self._interpolate(v)
            ret = re.sub(self.PROPERTY_PLACEHOLDER_RE, v, ret, 1)
        return ret

    def _interpolate_property(self, prop):
        try:
            ret = self._interpolate(self.raw_properties[prop])
        except KeyError as e:
            self.logger.error("KeyError %s, Property '%s' is not test environment", e, prop)
            ret = None
        self.logger.debug(f"{prop}={ret}")
        return ret

    def set_properties(self):
        for key in self.raw_properties.keys():
            value = self._interpolate_property(key)
            self.properties[key] = value

    def get_property(self, prop: str):
        ret = self.properties[prop]
        self.logger.info(f"{prop} = {ret}")
        return ret

    def add_property(self, key: str, value):
        self.properties[key] = value
