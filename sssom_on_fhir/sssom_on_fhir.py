"""Convert OWL to FHIR"""
import os
import shutil
import subprocess
from argparse import ArgumentParser
from copy import copy
from typing import Dict, List

import requests

SRC_DIR = os.path.realpath(os.path.dirname(__file__))
PROJECT_DIR = os.path.realpath(os.path.join(SRC_DIR, '..'))
CONTENT_DIR = os.path.realpath(os.path.join(PROJECT_DIR, 'content'))
RELEASE_DIR = os.path.realpath(os.path.join(PROJECT_DIR, 'release'))
REPO_URL = 'https://github.com/timsbiomed/sssom-on-fhir-content/'
LATEST_RELEASE_URL = REPO_URL + 'releases/latest/'
LATEST_RELEASE_API_URL = LATEST_RELEASE_URL.replace('github.com', 'api.github.com/repos')[:-1]
LATEST_RELEASE_DOWNLOAD_STEM = LATEST_RELEASE_URL + 'download/'  # filename goes after


def _run_shell_command(command: str, cwd: str = None) -> subprocess.CompletedProcess:
    """Runs a command in the shell, and handles some common errors"""
    args = command.split(' ')
    if cwd:
        result = subprocess.run(args, capture_output=True, text=True, cwd=cwd)
    else:
        result = subprocess.run(args, capture_output=True, text=True)
    stderr, stdout = result.stderr, result.stdout
    if stdout and 'error' in stdout or 'ERROR' in stdout:
        raise RuntimeError(stdout)
    if stderr:
        allowed_exceptions = [
            'ChainedAssignmentError'  # non-breaking; recovered from in sssom-py
        ]
        err = copy(stderr)
        for exc in allowed_exceptions:
            err = err.replace(exc, '')
        if any([x in err.lower() for x in ['error', 'exception', 'traceback']]):
            raise RuntimeError(stderr)
    return result


def _download_file(url: str, path: str):
    """Download a file"""
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise an exception if the request was unsuccessful
    with open(path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:  # filter out keep-alive new chunks
                file.write(chunk)


def stage_release(
    content_dir: str = CONTENT_DIR, release_dir: str = RELEASE_DIR, release_url: str = LATEST_RELEASE_API_URL
):
    """Gather all relevant files into release/ dir"""
    if not os.path.exists(release_dir):
        os.makedirs(release_dir)

    print('release: collecting .fhir.json files')
    for root, dirs, files in os.walk(content_dir):
        for file in files:
            if file.endswith('.fhir.json'):
                shutil.copy(os.path.join(root, file), release_dir)

    print('release: collecting .sssom.tsv files from storage in prior release (too large for git)')
    response = requests.get(release_url)
    if response.status_code == 200:
        release_data = response.json()
        assets = release_data.get('assets', [])
        to_dl = [a['browser_download_url'] for a in assets if a['name'].endswith('.sssom.tsv')]
        for url in to_dl:
            _download_file(url, os.path.join(release_dir, os.path.basename(url)))
    else:
        raise RuntimeError(
            f"Failed to fetch release data; needed to download TSVs from prior latest release storage to put in new "
            f"release:"
            f"\n - response code{response.status_code}" +
            f"\n - response text: {response.text}" +
            f"\n - response json: {str(response.json())}")


def sssom_to_fhir(
    inpath: str, outpath: str, dev_sssom_path: str = None, dev_sssom_interpreter_path: str = None,
) -> str:
    """Run conversion"""
    # Validate args
    if (dev_sssom_path and not dev_sssom_interpreter_path) or (not dev_sssom_path and dev_sssom_interpreter_path):
        raise ValueError('If you specify a `dev_sssom_path` or `dev_sssom_interpreter_path`, you must specify both.')

    # Contingencies
    if not os.path.exists(os.path.dirname(outpath)):
        os.makedirs(os.path.dirname(outpath))

    # Run conversion
    dev_sssom_path = dev_sssom_path if dev_sssom_path is None or not dev_sssom_path.endswith('sssom-py') \
        else os.path.join(dev_sssom_path, 'sssom', 'cli.py')
    cwd = os.path.realpath(os.path.join(os.path.dirname(dev_sssom_path), '..')) if dev_sssom_path else PROJECT_DIR
    lead_cmd = 'sssom' if not dev_sssom_path else f'{dev_sssom_interpreter_path} {dev_sssom_path}'
    command = f'{lead_cmd} convert {inpath} --output-format fhir_json --output {outpath}'
    _run_shell_command(command, cwd=cwd)

    return outpath


def convert_from_content_dir(dev_sssom_path: str = None, dev_sssom_interpreter_path: str = None):
    """Convert all the latest versions from the content/ dir

    This will go to the content/ dir look for all "content module" directories there and, within each, look at tsv/, get
    the highest "v#", and convert any tsv files there, placing them in the content module\'s corresponding fhir/ dir."""
    content_modules: List[str] = os.listdir(CONTENT_DIR)
    for module in content_modules:
        # Locate TSV to convert
        inpath = None
        tsv_dir = os.path.join(CONTENT_DIR, module, 'tsv')
        version_dirs = [d for d in os.listdir(tsv_dir) if d.startswith('v')]
        version_dir_map = {
            int(v.split('v')[-1]): os.path.join(tsv_dir, v)
            for v in version_dirs
        }
        highest_version = max(version_dir_map.keys())
        highest_version_dir = version_dir_map[highest_version]
        highest_version_dir_tsvs = [x for x in os.listdir(highest_version_dir) if x.endswith('.tsv')]
        missing_err = (f'No TSV files found in highest version directory (version number = {highest_version}) '
                       f'for content module {module}.')
        if not highest_version_dir_tsvs:
            # Likely the file was to big for git; can find in latest release
            filename = module + '.sssom.tsv'
            release_url = LATEST_RELEASE_DOWNLOAD_STEM + filename
            inpath = os.path.join(highest_version_dir, filename)
            try:
                _download_file(release_url, inpath)
            except requests.exceptions.HTTPError as err:
                if err.response.status_code == 404:
                    raise RuntimeError(missing_err) from err
                raise err
        elif len(highest_version_dir_tsvs) > 1:  # todo: support multiple per module
            raise NotImplementedError(f'More than one TSV file found in highest version directory (version number = '
                               f'{highest_version}) for content module {module}.')
        # Convert
        inpath = inpath if inpath else os.path.join(highest_version_dir, highest_version_dir_tsvs[0])
        filename_stem = os.path.basename(inpath.replace('.sssom.tsv', '').replace('.tsv', ''))
        outpath = os.path.join(CONTENT_DIR, module, 'fhir', filename_stem + '.fhir.json')
        sssom_to_fhir(inpath, outpath, dev_sssom_path, dev_sssom_interpreter_path)


def cli():
    """Command line interface."""
    package_description = 'Convert SSSOM to FHIR.'
    parser = ArgumentParser(description=package_description)
    parser.add_argument('-i', '--inpath', required=False, help='Path to input SSSOM TSV.')
    parser.add_argument('-o', '--outpath', required=False, help='Where FHIR ConceptMap JSON should be saved.')
    parser.add_argument(
        '-c', '--convert-from-content-dir', action='store_true', required=False,
        help='If this option is used, other CLI flags are ignored. This will go to the content/ dir look for all '
             '"content module" directories there and, within each, look at tsv/, get the highest "v#", and convert any '
             'tsv files there, placing them in the content module\'s corresponding fhir/ dir.')
    parser.add_argument(
        '-r', '--stage-release', action='store_true', required=False,
        help='If this option is used, other CLI flags are ignored. Will gather any *.fhir.json files into release/ dir')
    parser.add_argument(
        '-d', '--dev-sssom-path', default=None, required=False,
        help='If you want to use a local development version of SSSOM, specify the path to the OAK directory here. '
             'Must be used with --dev-sssom-interpreter-path.')
    parser.add_argument(
        '-D', '--dev-sssom-interpreter-path', default=None, required=False,
        help='If you want to use a local development version of SSSOM, specify the path to the Python interpreter '
             'where its dependencies are installed (i.e. its virtual environment). Must be used with --dev-sssom-path.')

    d: Dict = vars(parser.parse_args())
    if d['stage_release']:
        stage_release()
    elif d['convert_from_content_dir']:
        convert_from_content_dir()
    else:
        del d['convert_from_content_dir']
        if not (d['inpath'] and d['outpath']):
            raise RuntimeError('Required params missing: --inpath, --outpath')
        sssom_to_fhir(**d)


if __name__ == '__main__':
    cli()
