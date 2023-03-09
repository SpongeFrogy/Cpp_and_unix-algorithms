#!/bin/bash
VAR=$(date '+%d.%m.%Y.%H.%M.%S')
git checkout prd
git merge --commit stg 
git tag "$VAR"
git push origin prd
git push origin "$VAR"
