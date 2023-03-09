#!/bin/bash
VAR=$(date '+%d.%m.%Y.%H.%M.%S')
git checkout stg
git merge --commit dev 
git tag "$VAR"
git push origin stg
git push origin "$VAR"
