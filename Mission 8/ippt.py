# IPPT Helper Functions
#
_map = map
def map(fn, x):
    return tuple(_map(fn, x))

def make_ippt_table(pushup, situp, run):
    return (pushup, situp, run)
def get_pushup_table(ippt_table):
    return ippt_table[0]
def get_situp_table(ippt_table):
    return ippt_table[1]
def get_run_table(ippt_table):
    return ippt_table[2]

def create_table(data, row_keys, col_keys):
    def make_indexer(keys):
        def indexer(key):
            for i, k in enumerate(keys):
                if k == key:
                    return i
            return None
        return indexer

    return (data, make_indexer(row_keys), make_indexer(col_keys))

def row_indexer(table):
    return table[1]
def col_indexer(table):
    return table[2]
def get_data(table):
    return table[0]

def access_cell(table, row_key, col_key):
    data = get_data(table)
    row_idx = row_indexer(table)(row_key)
    col_idx = col_indexer(table)(col_key)

    if row_idx == None or col_idx == None:
        return None

    return data[row_idx][col_idx]
