""""Convert from v2 to v3"""
import os

import pandas as pd

THIS_DIR = os.path.realpath(__file__)
SRC_DIR = os.path.join(THIS_DIR, '..', '..', 'content', 'icd_snomed', 'tsv')
IN_DIR = os.path.join(SRC_DIR, 'input')
OUT_DIR = os.path.join(SRC_DIR, 'output')

# Modify original CSVs -------------------------------------------------------------------------------------------------
# TODO for all:
#  - remove column curi_map
#  - save individaul TSV just in case useful alternative to combined
#  - add comment w/ sssom metadata (including curie_map)
df177 = pd.read_csv(os.path.join(IN_DIR, 'sssom_mappings_177icd10cm.csv'), comment='#').fillna('')


df1411 = pd.read_csv(os.path.join(IN_DIR, 'sssom_mappings_1411icd10cm.csv'), comment='#').fillna('')


df1507 = pd.read_csv(os.path.join(IN_DIR, 'sssom_mappings_1507icd10cm.csv'), comment='#').fillna('')


df1578 = pd.read_csv(os.path.join(IN_DIR, 'sssom_mappings_1578icd10cm.csv'), comment='#').fillna('')


df1678 = pd.read_csv(os.path.join(IN_DIR, 'sssom_mappings_1678icd10cm.csv'), comment='#').fillna('')


df1688 = pd.read_csv(os.path.join(IN_DIR, 'sssom_mappings_1688icd10cm.csv'), comment='#').fillna('')


df1726 = pd.read_csv(os.path.join(IN_DIR, 'sssom_mappings_1726icd10cm.csv'), comment='#').fillna('')


df1726a = pd.read_csv(os.path.join(IN_DIR, 'sssom_mappings_1726icd10cm_a.csv'), comment='#').fillna('')


df1726b = pd.read_csv(os.path.join(IN_DIR, 'sssom_mappings_1726icd10cm_b.csv'), comment='#').fillna('')


df1793 = pd.read_csv(os.path.join(IN_DIR, 'sssom_mappings_1793icd10cm.csv'), comment='#').fillna('')


df1798 = pd.read_csv(os.path.join(IN_DIR, 'sssom_mappings_1798icd10cm.csv'), comment='#').fillna('')


df1507s = pd.read_csv(os.path.join(IN_DIR, 'sssom_sample_1507icd10cm.csv'), comment='#').fillna('')


# Save new CSVs and metadata yml ---------------------------------------------------------------------------------------
# TODO: come up w the best metadata yml based on each file and save each file

# Concat, add yaml comment, and save -----------------------------------------------------------------------------------
