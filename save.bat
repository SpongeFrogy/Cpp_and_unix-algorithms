git checkout stg
@pause
git merge --commit dev 
@pause
git push
@pause
git checkout prd
@pause
git merge --commit stg
@pause
git push
@pause
git switch main
@pause