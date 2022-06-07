import logging

import requests

logger = logging.getLogger(__name__)


# csv form ELK - aggregated over buckets - avg,min,max as for duration
class MMMDbMetrics:
    def __init__(self, catalog_items, profiled_pct):
        self.catalogItems = catalog_items
        self.profiledPct = profiled_pct


# from index.json
# GQL_ORDER = 'gqlOrder'
# GQL_HASH_MD5 = 'gqlHashMD5'
# GQL_LENGTH = 'gqlLength'
# GQL_VARIABLES_LENGTH = 'variablesLength'
# GQL_VARIABLES_HASH_MD5 = 'variablesHashMD5'
# GQL_FE_TRANSACTION = 'uiTransaction'
OPERATION_NAME = 'operationName'


# loaded from csv from ELK
class ElkGqlStats:
    def __init__(self, mean, median, maximum):
        self.mean = mean
        self.median = median
        self.max = maximum
        self.count = 0
        # has is MD5 hash i.e string
        self.hash = ''
        self.stdDevLower = 0
        self.stdDevUpper = 0


class ElkGqlTrxStats(ElkGqlStats):
    def __init__(self, mean, median, maximum):
        super().__init__(mean, median, maximum)
        self.feTransaction = None


class ElkGqlOpNameStats(ElkGqlStats):
    def __init__(self, mean, median, maximum):
        super().__init__(mean, median, maximum)
        self.operationName = None


# loaded from index.json created by parse_gqls.py
class GQLParameters:
    def __init__(self, operation_name, gql_hash, length):
        self.operationName = operation_name
        # hash of GQL with removed whitespaces
        self.hash = gql_hash
        self.length = length
        self.feTransaction = None
        # growing counter of duplicated GQLs per operationName  (new)
        self.order = 0
        # growing counter of duplicated GQLs regardless of operationName (old)
        self.count = 0
        # whitespaces removed
        self.variablesLength = 0


def post_gql(url, user, password, data):
    r = requests.post(url, auth=(user, password), verify=False, json=data)
    if r.status_code != 200:
        return None
    returned_data = r.json()['data']['_buildInfo']
    logger.debug("Returned data %s", returned_data)
    return returned_data
