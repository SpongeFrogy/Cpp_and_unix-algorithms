cd C:\Users\droid\Projects\6sem_Cpp_and_unix
@pause
git switch main
@pause
git add -A
@pause
git commit -m script_commit
@pause
git push
@pause
git switch dev
git reset
@pause
git merge --commit main
@pause
git add -A
@pause
git commit -m script_commit
@pause
git push 
git switch stg
git reset
@pause
git merge --commit dev
@pause
git add -A
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
