"""Convert OWL to FHIR"""
import os
from argparse import ArgumentParser
from collections import OrderedDict
from typing import Dict, List


# Vars
# - Vars: Static
SRC_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(SRC_DIR, '..')
CONTENT_DIR = os.path.join(PROJECT_DIR, '..', 'content')

# - Vars: Config
# TODO: customize properly
FAVORITE_DEFAULTS = {
    'out_dir': os.path.join(CONTENT_DIR, 'output'),
    'intermediary_outdir': os.path.join(CONTENT_DIR, 'input'),
    'include_all_predicates': True,
    'intermediary_type': 'obographs',
    'use_cached_intermediaries': True,
    'retain_intermediaries': True,
    'convert_intermediaries_only': False,
}
# TODO: customize properly
FAVORITES = OrderedDict({
    'icd_snomed': {
        'download_url': None,
        'input_path': os.path.join(CONTENT_DIR, 'input', 'mondo.owl'),
        # '_id': '',
        # 'native_uri_stems': ['http://purl.obolibrary.org/obo/_'],
    },
})


# TODO: customize properly
def sssom_to_fhir(
    input_path_or_url: str, out_dir: str = CONTENT_DIR, out_filename: str = None, include_all_predicates=False,
    retain_intermediaries=False, intermediary_type=['obographs', 'semsql'][0], use_cached_intermediaries=False,
    intermediary_outdir: str = None, convert_intermediaries_only=False, native_uri_stems: List[str] = None,
    code_system_id: str = None, code_system_url: str = None, dev_sssom_path: str = None,
    dev_sssom_interpreter_path: str = None
) -> str:
    """Run conversion"""
    outpath = ''
    return outpath


# todo
# def _run_favorites(
#     use_cached_intermediaries: bool = None, retain_intermediaries: bool = None, include_all_predicates: bool = None,
#     intermediary_type: str = None, out_dir: str = None, intermediary_outdir: str = None,
#     convert_intermediaries_only: bool = None, dev_sssom_path: str = None, dev_sssom_interpreter_path: str = None,
#     favorites: Dict = FAVORITES
# ):
#     """Convert favorite ontologies"""
#     kwargs = {k: v for k, v in locals().items() if v is not None and not k.startswith('__') and k != 'favorites'}
#     fails = []
#     successes = []
#     n = len(favorites)
#     i = 0
#     for d in favorites.values():
#         i += 1
#         print('Converting {} of {}: {}'.format(i, n, d['code_system_id']))
#         try:
#             sssom_to_fhir(
#                 out_filename=f'CodeSystem-{d["code_system_id"]}.json',
#                 input_path_or_url=d['input_path'] if d['input_path'] else d['download_url'], **kwargs)
#             successes.append(d['id'])
#         except Exception as e:
#             fails.append(d['code_system_id'])
#             print('Failed to convert {}: \n{}'.format(d['code_system_id'], e))
#     print('SUMMARY')
#     print('Successes: ' + str(successes))
#     print('Failures: ' + str(fails))


# TODO: customize properly
def cli():
    """Command line interface."""
    package_description = 'Convert SSSOM to FHIR.'
    parser = ArgumentParser(description=package_description)
    parser.add_argument('-i', '--input-path-or-url', required=False, help='URL or path to OWL file to convert.')
    # parser.add_argument(
    #     '-o', '--out-dir', required=False, default=CONTENT_DIR, help='The directory where results should be saved.')
    parser.add_argument(
        '-n', '--out-path', required=False, help='Path to create output SSSOM ConceptMap FHIR JSON.')
    # parser.add_argument(
    #     '-s', '--code-system-id', required=False, default=False,
    #     help="For `fhirjson` only. The code system ID to use for identification on the server uploaded to. "
    #          "See: https://hl7.org/fhir/resource-definitions.html#Resource.id",)
    # parser.add_argument(
    #     '-S', '--code-system-url', required=False, default=False,
    #     help="For `fhirjson` only. Canonical URL for the code system. "
    #          "See: https://hl7.org/fhir/codesystem-definitions.html#CodeSystem.url",)
    # parser.add_argument(
    #     '-u', '--native-uri-stems', required=False, nargs='+',
    #     help='A comma-separated list of URI stems that will be used to determine whether a concept is native to '
    #          'the CodeSystem. For example, for OMIM, the following URI stems are native: '
    #          'https://omim.org/entry/,https://omim.org/phenotypicSeries/PS"'
    #          'As of 2023-01-15, there is still a bug in the Obographs spec and/or `robot` where certain nodes are not'
    #          ' being converted. This converter adds back the nodes, but to know which ones belong to the CodeSystem '
    #          'itself and are not foreign concepts, this parameter is necessary. OAK also makes use of this parameter.'
    #          ' See also: https://github.com/geneontology/obographs/issues/90')
    parser.add_argument(
        '-d', '--dev-sssom-path', default=False, required=False,
        help='If you want to use a local development version of SSSOM, specify the path to the OAK directory here. '
             'Must be used with --dev-sssom-interpreter-path.')
    parser.add_argument(
        '-D', '--dev-sssom-interpreter-path', default=False, required=False,
        help='If you want to use a local development version of SSSOM, specify the path to the Python interpreter '
             'where its dependencies are installed (i.e. its virtual environment). Must be used with --dev-sssom-path.')
    # parser.add_argument(
    #     '-f', '--favorites', action='store_true', default=False, required=False,
    #     help='If present, will run all favorite ontologies found in `FAVORITES`. If using this option, the '
    #          'other CLI flags are not relevant. Instead, edit the following config: `FAVORITE_DEFAULTS`.')

    d: Dict = vars(parser.parse_args())
    # if d['favorites']:
    #     _run_favorites(
    #         dev_sssom_path=d['dev_sssom_path'], dev_sssom_interpreter_path=d['dev_sssom_interpreter_path'],
    #         **{**FAVORITE_DEFAULTS, **{'favorites': FAVORITES}})
    # del d['favorites']
    sssom_to_fhir(**d)


# Execution
if __name__ == '__main__':
    cli()
