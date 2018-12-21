## DSE

* File exists: `/predictions.csv`

## TA1
* File exists: `/metadata.yml`
* `==1` files match `/predictions/*/predictions.csv`
* `==1` files match `/pipelines/*.json`
* `==1` files match `/executables/*.*`
* `/pipelines/$id.json` must exist for each `/predictions/$id/predictions.csv`
* `/pipelines/$id.json` must exist for each `/executables/$id.*`

NB: Not checking for the optional directories `supporting_files`, `subpipelines`

## TA2
* File exists: `/metadata.yml`
* `>0` files match `/predictions/*/predictions.csv`
* `>0` files match `/pipelines/*.json`
* `>0` files match `/executables/*.*`
* `/pipelines/$id.json` must exist for each `/predictions/$id/predictions.csv`
* `/pipelines/$id.json` must exist for each `/executables/$id.*`

NB: Not checking for the optional directories `supporting_files`, `subpipelines`, `pipelines_considered`


## TA3+2 Task 1
* File exists: `/metadata.yml`
* File exists: `/problems/labels.csv`
* `>0` files match `/problems/*/schema.json`
* `>0` files match `/problems/*/ssapi.*`
* `/problems/$id/schema.json` must exist for each `/problems/$id/ssapi.*`
* `/problems/$id/ssapi.*` must exist for each `/problems/$id/schema.json`
* `/problems/$id/ssapi.*` must match 1 file per $id

## Ta3+2 Task 2
* File exists: `/metadata.yml`
* `>0` files match `/predictions/*/predictions.csv`
* `>0` files match `/pipelines/*.json`
* `>0` files match `/executables/*.*`
* `/pipelines/$id.json` must exist for each `/predictions/$id/predictions.csv`
* `/pipelines/$id.json` must exist for each `/executables/$id.*`

NB: Not checking for the optional directories `supporting_files`, `subpipelines`, `pipelines_considered`