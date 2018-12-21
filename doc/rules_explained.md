TODO got this page from the wiki, it's out of date

`Rule = (Matching -> (Context)*)-> Action+ `

## Matching

```yml
- path_matches: "path/to/file.ext"
```

```yml
- path_matches:
    path: "path/to/file.ext"
```

```yml
- path_matches: FILEPATH
  exists: true
```

* Matches by filepath, absolute or relative
* Context: 0-1 file paths
* Checks:
  * Path exists at FILEPATH

### Exists and is file
```yml
- file_exists: FILEPATH
```

```yml
- path_exists: FILEPATH
  type: file
```

```yml
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

```yml
- dir_exists: FILEPATH
```

```yml
- path_exists: FILEPATH
  type: dir
```

```yml
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
```yml
- exists:
    - source_file: SOURCEFILE.txt
  type: dir
```

```yml
- paths:
      - FILEPATH1
      - FILEPATH2
  type: file
```

```yml
- path_matches:  x/*.ext
```

```yml
- path_matches_list:
    - x/*.ext
    - y/*.sh
```
