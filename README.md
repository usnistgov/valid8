[![pipeline][badge_pipeline]][git_url]
[![coverage][badge_coverage]][coverage_report]

[badge_pipeline]: https://gitlab.com/prometheuscomputing/rules-based-validator/badges/master/pipeline.svg
[badge_coverage]: https://gitlab.com/prometheuscomputing/rules-based-validator/badges/master/coverage.svg
[git_url]: https://gitlab.com/prometheuscomputing/rules-based-validator
[coverage_report]: https://prometheuscomputing.gitlab.io/rules-based-validator/_static/coverage/index.html

`rbv` will check whether a directory structure meets a list of rules defined in a configuration `rules.yml` file.

## Installation

```bash
$ git clone $GIT_URL
$ pip install rules-based-validator
```

## Usage

```bash
$ rbv validate [--directory directory] rules.yml
$ rbv lint rules.yml
```

An example `rules.yml`
```yaml
- rulename: arbitraryrulename
  filters:
    path_list:
      - "Makefile"
      - "setup.py"
      - "rbv/cli.py"
  actions:
    exists: true
```

## Filters and Actions

Each rule is described by two different concepts:
* **Filters** select the files to which the rule will be applied..
* **Actions** run checks on the files selected by the filters.

Each rule is considered valid if all actions taken on the files
selected by the filters returned a 0 exit code (success).

### Filters


|  Name   | Usage         | Description                                        | Status  |  
|---------|---------------|----------------------------------------------------|---|
| path    | `path: "*.json"`  | Find files by a single name or pattern.  | Stable  |   
| path_list | `path_list:`<br/>`    - "hello.txt"`<br/>`    - "*.py"` | Find files from list of names or patterns. | Stable  |   
| paths_from_file  | `paths_from_file: "file_with_paths.txt"`| Find files from file with names or patterns, one per line.  | Beta  |   

N.B. Compatible pattern matching expressions: anything compatible with `glob`


### Actions

|  Name   | Usage         | Description                                        | Status  |  
|---------|---------------|----------------------------------------------------|---|
| exists  | `exists: True`| Selected files exist (e.g. a minimum of 1 found)   | Stable  |   
| count   | `count: n`    | Find exactly `n` selected files.                   | Stable  |   
| match   | `match: {DIR_NAME}/otherfile.txt`            | For each selected file, find another matched file  | Stable  |   

#### Substitutions

*N.B.* Only available in `action.match`

In some rules, it may be necessary to use information about the filtered files to make a determination on an action. The substitutions keys below are available for use in the parameter of the `match` action.

For example, the following will check that every file matching `predictions/*/predictions.csv` has a corresponding `JSON` file with the original directory name as its filename.

```yaml
- rulename: predictions_file
  filters:
    path: "predictions/*/predictions.csv"
  actions:
    match: "pipelines/{DIR_NAME}.json"
```

Examples are based on the file path `a/b/c.txt`

| Substitution keys  |   Description                      |Example value|
|--------------------|------------------------------------|-------------|
| `{DIR_NAME}`       |  the directory name                | `b`         |
| `{DIR_PATH}`       |  the directory path                | `a/b`       |
| `{FILENAME_NOEXT}` | the filename without the extension | `c`         |
| `{FILENAME}`       | the filename with the extension    | `c.txt`     |
| `{FILEPATH}`       | the file path                      | `a/b/c.txt` |


### Adding a custom filter or action

1. Add the code in `filters/` or `actions/` respectively.
2. Each filter or action must be a function and must include the `context` parameter in the signature.
3. In the `filters/` or `actions/` `__init__.py`, add an import to add the new function under the
`filters` or `actions` module.
Name must be unique
