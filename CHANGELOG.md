# Changelog

## v1.2

**Core**: 
* `count` action now supports `count: 1+` syntax
* Using `pyyaml` `safe_load` instead of `load`
* No longer using `subprocess` `shell=True` option

**Misc**:

* Docs are now hosted on NIST-pages 
* `push_to_gitlab` CI pipelines can be triggered on `web` CI pipelines. 

## v1.1

**Date**: Feburary 7th, 2019

* Renamed the package and cli to 'valid8'
* The CLI call `valid8 validate` is renamed `valid8 apply`
* `rbv` CLI command still works but the `validate` portion is also now `rbv apply` 
* Improved CLI help message

## v1.0

**Date**: Feburary 5th, 2019

Initial release.

Supports: 
* YAML-specified rules 
* `rbv` CLI 
* Usage: `rbv [-d path/to/dir rules.yml`

 
