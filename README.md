# valid8: Human Readable Validation

`valid8` interprets rules in a human-readable format (YAML) and applies those rules to a directory structure.

## Installation

This package requires Python3.6+.

Clone the repository and use pip to install the contents:
```bash
$ git clone [GIT_CLONE_URL]
$ pip install -r valid8/requirements.txt
$ pip install ./valid8
```

## Usage

`valid8` supports two subcommands:
* `validate` for most uses
* `lint` to check the validity of the rules file

Usage:
```bash
$ valid8 apply [--directory directory] rules.yml
$ valid8 lint rules.yml
```


## Example rules file

Example `rules.yml` with one rule:
```yaml
- rulename: count_lines_in_specified_files
  filters:
    path_list:
      - "Makefile"
      - "setup.py"
      - valid8
  actions:
    exists: true
    scripts:
      - wc -l ${FILEPATH}
```

Other examples can be found in the `examples/` folder.

## Filters and Actions

Each rule is described by two different concepts:
* **Filters** select the files to which the rule will be applied.
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


#### The `find` shortcut

The `find` filter is also available as syntactic sugar for the `path`, `path_list` and `paths_from_file` filters.


Using `find` with a direct argument calls `path`
```yaml
  filters:
    find: find_this_file.txt
```

Using `find` with a YAML list calls `path_list`

```yaml
  filters:
    find:
      - find_this_file.txt
      - also_these_files.*
```

Using `find` with a YAML mapping and the key `file` calls `path_from_file`

```yaml
  filters:
    find:
      file: file_with_paths.txt
```

These modes are not combinable. Only use one per rule.

### Actions

|  Name   | Usage         | Description                                        | Status  |  
|---------|---------------|----------------------------------------------------|---|
| exists  | `exists: True`| Selected files exist (e.g. a minimum of 1 found)   | Stable  |   
| count   | `count: n`    | Find exactly `n` selected files.                   | Stable  |   
| match   | `match: {DIR_NAME}/otherfile.txt`               | For each selected file, find another matched file       | Stable  |   
| scripts (inline) | `scripts: "wc -l {FILEPATH}"`          | Execute a shell command for each selected file          | Stable  |   
| scripts (list)   | `scripts:`<br/>`  - wc -l {FILEPATH}`  | Execute a list of shell commands for each selected file | Stable  |   

#### Substitutions

*N.B.* Only available in `action.match` and `action.scripts`

In some rules, it's useful to use information about the filtered files to make a determination on an action. The substitutions keys below are available for use in the parameter of the `match` and `scripts` action.

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

## About

**License**

The license is documented in the [LICENSE file](LICENSE.txt) and on the [NIST website](https://www.nist.gov/director/copyright-fair-use-and-licensing-statements-srd-data-and-software).

**Versions and releases**:

See
* the repository tags for all releases. [Gitlab link](/../tags) [Github link](../../tags)
* the [CHANGELOG file](CHANGELOG.md) for a history of the releases.
* [the `__version__` field in `valid8/__init__.py`](valid8/__init__.py).

**Contact**:

Please send any issues, questions, or comments to datascience@nist.gov

**Authors**:

* Marion Le Bras
