""""Convert from v2 to v3"""
import dateutil.parser as dp
import os
import yaml
from typing import Any, Dict, List

import pandas as pd


THIS_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.join(THIS_DIR, '..', '..', 'content', 'icd_snomed', 'tsv')
IN_DIR = os.path.join(SRC_DIR, 'v2')
OUT_DIR_V3 = os.path.join(SRC_DIR, 'v3')
OUT_DIR_V4 = os.path.join(SRC_DIR, 'v4')

# Read and write metadata
# - read and save new metadata.yaml ------------------------------------------------------------------------------------
metadata_inpath = os.path.join(IN_DIR, 'metadata.yaml')
with open(metadata_inpath, 'r') as stream:
    metadata: Dict[str, Any] = yaml.safe_load(stream)
with open(os.path.join(OUT_DIR_V3, 'metadata.yaml'), 'w') as stream:
    yaml.dump(metadata, stream)
with open(os.path.join(OUT_DIR_V4, 'metadata.yaml'), 'w') as stream:
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
    df = pd.read_csv(os.path.join(IN_DIR, path), comment='#')
    outpath = os.path.join(OUT_DIR_V3, os.path.basename(path).replace('.csv', '.tsv'))
    # drop col
    df = df.drop(columns=['curi_map'])
    # drop empty rows
    df = df.dropna()
    # reformat dates
    df['mapping_date'] = df['mapping_date'].apply(lambda x: dp.parse(x).strftime('%Y-%m-%d'))
    # fix malformatted CURIEs
    df['object_id'] = df['object_id'].apply(
        lambda x: x.replace('Cancer Modifier', 'cancer_modifier')
        .replace('OMOP Extension', 'omop_extension'))
    # todo: sort values?
    pass
    # save & return
    # - add comments
    if os.path.exists(outpath):
        os.remove(outpath)
    f = open(outpath, 'a')
    f.write(metadata_str)
    f.close()
    # - save data & return
    df.to_csv(outpath, index=False, sep='\t', mode='a')
    datasets_list.append(df)

# Concat, add yaml comment, and save -----------------------------------------------------------------------------------
# todo: new column 'set name' based on _id above? Ask steph but i dont think needed?
# todo: drop duplicates? based on which cols? all?
# todo: sort?
df_all = pd.concat(datasets_list)
outpath_all = os.path.join(OUT_DIR_V4, 'icd10cm_snomed_from_omop.sssom.tsv')
if os.path.exists(outpath_all):
    os.remove(outpath_all)
f = open(outpath_all, 'a')
f.write(metadata_str)
f.close()
df_all.to_csv(outpath_all, index=False, sep='\t', mode='a')
