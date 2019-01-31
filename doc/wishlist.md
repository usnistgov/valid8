# Feature wishlist

## Linter
Make the linter better. Currently cannot check action/filter sub-syntax.

## Markup

### Allow jinja2 templates
like in ansible yaml files

### Allow for more than yml as markup

### Syntax change so we can use the same action more than once per rule
Currently action uses key-value to list actions, the key being the action name.
Possible change: use key-list of key-value. Syntax change.

## CLI

### Apply on more than one directory structure
```bash
rbv [-v] rules.yml --apply dir_or_file1 [dir_or_file1, ...]
```


## Filters, Actions

### More filters


### More actions

* count/cardinality
* type check 


## Engine

### Custom filters and actions
Support adding filters and actions from external location (e.g. `--lib custom`)

### Queuing
instead of having the engine directly call an action, have it push it to a queue that a worker will then pick-up (consumer-producer)

### Rules_d reorganization
Include contexts in rules_d
Drop the s in contexts
Have the actions output be in rules_d, subdir matching context(s)
