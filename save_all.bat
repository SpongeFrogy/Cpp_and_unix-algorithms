cd C:\Users\droid\Projects\6sem_Cpp_and_unix
git switch main
git add -A
git commit -m script_commit
git push
git switch dev
echo The echoed text
@pause
git merge --commit main
git add -A
git commit -m script_commit
git push 
git switch stg
echo The echoed text
@pause
git merge --commit dev
echo The echoed text
@pause
git add -A
git commit -m script_commit
echo The echoed text
@pause
git push   
git switch prd
git merge --commit stg
git add -A
git commit -m script_commit
git push 
git switch main
