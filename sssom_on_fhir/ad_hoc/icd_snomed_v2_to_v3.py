""""Convert from v2 to v3"""
import os
import yaml
from typing import Any, Dict, List

import pandas as pd


THIS_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.join(THIS_DIR, '..', '..', 'content', 'icd_snomed', 'tsv')
IN_DIR = os.path.join(SRC_DIR, 'v2')
OUT_DIR = os.path.join(SRC_DIR, 'v3')

# Read and write metadata
# - read and save new metadata.yaml ------------------------------------------------------------------------------------
metadata_inpath = os.path.join(IN_DIR, 'metadata.yaml')
with open(metadata_inpath, 'r') as stream:
    metadata: Dict[str, Any] = yaml.safe_load(stream)
with open(os.path.join(OUT_DIR, 'metadata.yaml'), 'w') as stream:
    yaml.dump(metadata, stream)
# - generate comment string to go at top of TSVs
f = open(metadata_inpath, "r")
lines = f.readlines()
f.close()
output_lines = []
for line in lines:
    output_lines.append("# " + line)
metadata_str = ''.join(output_lines)

# Read and mutate CSVs, add comments, and save -------------------------------------------------------------------------
datasets_list = []
csv_paths: List[str] = [x for x in os.listdir(IN_DIR) if x.endswith('.csv')]
for path in csv_paths:
    # read
    # _id = path.replace('sssom_mappings_', '').replace('icd10cm.csv', '')
    df = pd.read_csv(os.path.join(IN_DIR, path), comment='#').fillna('')
    outpath = os.path.join(OUT_DIR, os.path.basename(path).replace('.csv', '.tsv'))
    # drop col
    df = df.drop(columns=['curi_map'])
    datasets_list.append(df)
    # todo: sort values?
    # add comments
    f = open(outpath, 'a')
    f.write(metadata_str)
    f.close()
    # save
    df.to_csv(outpath, index=False, sep='\t', mode='a')

# Concat, add yaml comment, and save -----------------------------------------------------------------------------------
# todo: new column 'set name' based on _id above? Ask steph but i dont think needed?
# todo: drop duplicates? based on which cols? all?
# todo: sort?
df_all = pd.concat(datasets_list)
outpath_all = os.path.join(OUT_DIR, 'combined', 'sssom_mappings_icd10cm.tsv')
f = open(outpath_all, 'a')
f.write(metadata_str)
f.close()
df_all.to_csv(outpath_all, index=False, sep='\t', mode='a')
