""""Convert from v2 to v3"""
import os
from typing import List

import pandas as pd

THIS_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.join(THIS_DIR, '..', '..', 'content', 'icd_snomed', 'tsv')
IN_DIR = os.path.join(SRC_DIR, 'v1')
OUT_DIR = os.path.join(SRC_DIR, 'v2')

# Read and mutate CSVs -------------------------------------------------------------------------------------------------
datasets = {}
csv_paths: List[str] = [x for x in os.listdir(IN_DIR) if x.endswith('.csv')]
for path in csv_paths:
    _id = path.replace('sssom_mappings_', '').replace('icd10cm.csv', '')
    df = pd.read_csv(os.path.join(IN_DIR, path), comment='#').fillna('')
    datasets[_id] = {'inpath': path, 'df': df}

# TODO for all:
#  - remove column curi_map
#  - save individaul TSV just in case useful alternative to combined
#  - add comment w/ sssom metadata (including curie_map)
# TODO contingent
#  - extract second row first col which is curie_map if exists
for _id, keys in datasets.items():
    df, inpath = keys['df'], keys['inpath']
    print()

print()
# Save new CSVs and metadata yml ---------------------------------------------------------------------------------------
# TODO: come up w the best metadata yml based on each file and save each file

# Concat, add yaml comment, and save -----------------------------------------------------------------------------------
