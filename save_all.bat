git switch main
git add -A
git commit -m script_commit
git push
git switch dev
git merge --commit main
git add -A
git commit -m script_commit
git push 
git switch stg
git merge --commit dev
git add -A
git commit -m script_commit
git push   
git switch prd
git merge --commit stg
git add -A
git commit -m script_commit
git push 
@pause