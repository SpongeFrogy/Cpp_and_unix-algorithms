git checkout main 
git add -A
git commit -m script_commit
git push
git checkout dev
git merge --commit main 
git add -A
git commit -m script_commit
git push dev
git checkout stg
git merge --commit dev 
git add -A
git commit -m script_commit
git push stg
git checkout prd
git merge --commit stg
git add -A
git commit -m script_commit 
git push prd


