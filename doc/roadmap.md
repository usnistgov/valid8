## First prototype

* Basic syntax for rules markup
* CLI
  * Inputs:
    * Rules markup
  * Outputs:
    * Summary log
```bash
rbv rules.yml
```

* One filter (3 sub-filters): matching file patterns
* One action: checking for file existence


## Enhancements

Unordered.

### Rules_d reorganization
Include contexts in rules_d
Drop the s in contexts
Have the actions output be in rules_d, subdir matching context(s)

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


