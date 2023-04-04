git checkout main 
git add -A
git commit -m script_commit
git push
git checkout dev
git merge --commit main 
git push origin dev
git checkout stg
git merge --commit dev 
git push origin stg
git checkout prd
git merge --commit stg 
git push origin prd


