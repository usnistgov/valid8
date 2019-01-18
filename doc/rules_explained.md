TODO got this page from the wiki, it's out of date

`Rule = (Matching -> (Context)*)-> Action+ `

## Matching

```yaml
- path_matches: "path/to/file.ext"
```

```yaml
- path_matches:
    path: "path/to/file.ext"
```

```yaml
- path_matches: FILEPATH
  exists: true
```

* Matches by filepath, absolute or relative
* Context: 0-1 file paths
* Checks:
  * Path exists at FILEPATH

### Exists and is file
```yaml
- file_exists: FILEPATH
```

```yaml
- path_exists: FILEPATH
  type: file
```

```yaml
- path: FILEPATH
  type: file
  exists: true
```

* Matches by filepath, absolute or relative
* Context: 0-1 file paths
* Checks:
  * Path exists at FILEPATH
  * FILEPATH is a file

NB: we can assume that `exists: true` is the default desired specification and omit it in most cases

### Directory existence

```yaml
- dir_exists: FILEPATH
```

```yaml
- path_exists: FILEPATH
  type: dir
```

```yaml
- path: FILEPATH
  type: dir
  exists: true
```

* Matches by filepath, absolute or relative
* Context: 0-1 file paths
* Checks:
  * Path exists at FILEPATH
  * FILEPATH is a directory

### Multiple file existence
```yaml
- exists:
    - source_file: SOURCEFILE.txt
  type: dir
```

```yaml
- paths:
      - FILEPATH1
      - FILEPATH2
  type: file
```

```yaml
- path_matches:  x/*.ext
```

```yaml
- path_matches_list:
    - x/*.ext
    - y/*.sh
```
