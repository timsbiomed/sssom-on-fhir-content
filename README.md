# sssom-on-fhir-content
SSSOM static files and conversion tools.

Potentially just a temporary library. Current use cases:
- Functional, easy to use converter while `sssom-py`'s FHIR functionality is still being developed.
- Ad hoc mutations of source files (programmatic and documented manual steps).

## Adding content
For new content, do the following:
1. Choose a name for your content module. There should be one input/output file per module. For example, if your output 
file is going to be called `example.fhir.json`, then you should call your input file `example.sssom.tsv`, and the module
name would be `example`..
2. Create a directory with the name of the content module.
3. Inside of that, create a `tsv/` directory. This Shoudl have 1 or more `v#` directories, each containing a version of 
the TSV. Put the latest version in the highest number. E.g. if you have 11 versions, you'd create `v1/`, `v2/`, ..., 
`v11/`. The highest version is the only one that will be converted.
4. Run the converter. You can run by manually setting the `--inpath` and `--outpath` flags, or if you run a new build, 
it will automatically find and convert your file for you.

## Running
From the cloned directory, run: `python3 -m sssom_on_fhir FLAGS`

To run the default conversion of everything in the `content/` directory, run: `python3 -m sssom_on_fhir -c`, or 
`make build`.

### CLI
| flag | long flag                  | description                                                                                                                                                                                                                                                                                 |
|------|----------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| -i   | --inpath                   | Path to input SSSOM TSV.                                                                                                                                                                                                                                                                    |
| -o   | --outpath                  | Where FHIR ConceptMap JSON should be saved.                                                                                                                                                                                                                                                 |
| -c   | --convert-from-content-dir | If this option is used, other CLI flags are ignored. This will go to the content/ dir look for all 'content module' directories there and, within each, look at tsv/, get the highest 'v#', and convert any tsv files there, placing them in the content module\'s corresponding fhir/ dir. |
