cd C:\Users\droid\Projects\6sem_Cpp_and_unix
git switch main
git add -A
git commit -m script_commit
git push
git switch dev
git reset
git merge --commit main
git add -A
git commit -m script_commit
git push 
git switch stg
@pause
git reset
@pause
git merge --commit dev
@pause
git add -A
@pause
git commit -m script_commit
@pause
git push   
git switch prd
git reset
git merge --commit stg
git add -A
git commit -m script_commit
git push 
git switch main
@pause