git checkout stg
git merge --commit dev 
git push
git checkout prd
git merge --commit stg
git push
git switch main