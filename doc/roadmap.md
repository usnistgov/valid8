
## First prototype

* Basic syntax for rules markup
* CLI
  * Inputs:
    * Rules markup
    * Directory to apply rules to
  * Outputs:
    * Return code 0/1
    * Summary log
```bash
rbv rules.yml
```

* One filter (3 sub-filters): matching file patterns
* One action: checking for file existence


## Enhancements

Unordered.

### Linter
Need a linter tool to validate yml markup

### Allow for more than yml as markup

### Can use the same action more than once per rule
Currently action uses key-value to list actions, the key being the action name.
Possible change: use key-list of key-value. Syntax change.

### Variable target
Currently rules apply in execution directory.

### Better CLI
```bash
rbv [-v] rules.yml --apply dir_or_file1 [dir_or_file1, ...]
```

### More filters


### More actions

* count/cardinality

### Custom filters and actions
Support adding filters and actions from external location (e.g. `--lib custom`)

### Queuing
instead of having the engine directly call an action, have it push it to a queue that a worker will then pick-up (consumer-producer)
