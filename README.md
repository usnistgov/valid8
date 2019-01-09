# Rules Based Validator

`rbv` will check whether a directory structure meets a list of rules defined
 in a configuration `rules.yml` file.
 
## Installation

```bash
$ git clone $GIT_URL
$ cd rules-based-validator
$ make install
```

## Usage 

```bash
$ rbv rules.yml
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
* One or more *filters* will select the files to which the rule will be applied.
* One or more *actions* will be taken on the selected files. 

Each rule is considered valid if all actions taken on the files 
selected by the filters returned a 0 exit code (success).

### Filters


|  Name   | Usage         | Description                                        | Status  |  
|---------|---------------|----------------------------------------------------|---|
| path    | `path: "*.json"`  | Find files by a single name or pattern.  | Stable  |   
| path_list | `path_list:`<br/>`    - "hello.txt"`<br/>`    - "*.py"` | Find files from list of names or patterns. | Stable  |   
| paths_from_file  | `paths_from_file: file_with_paths.txt`| Find files from file with names or patterns, one per line.  | Beta  |   

N.B. Compatible pattern matching expressions: anything compatible with `glob`


### Actions

|  Name   | Usage         | Description                                        | Status  |  
|---------|---------------|----------------------------------------------------|---|
| exists  | `exists: True`| Selected files exist (e.g. a minimum of 1 found)   | Stable  |   
| count   | `count: n`    | Find exactly `n` selected files.                   | Planned  |   
| match   | ``            | For each selected file, find another matched file  | Planned  |   


### Adding a custom filter or action

1. Add the code in `filters/` or `actions/` respectively. 
2. Each filter or action must be a function and must include the `context` parameter in the signature.
3. In the `filters/` or `actions/` `__init__.py`, add an import to add the new function under the 
`filters` or `actions` module. 
Name must be unique

