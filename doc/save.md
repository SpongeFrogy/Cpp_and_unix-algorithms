### [SAVE] Результат всех вышеперечисленных шагов сохранить в репозиторий

Фиксацию ревизий производить строго через ветку dev. С помощью скриптов
накатить ревизии на stg и на prd. Скрипты разместить в корне репозитория. Также
создать скрипты по возврату к виду текущей ревизии (даже если в папке имеются
несохраненные изменения + новые файлы).

выполняют 2 скрипта:

`save.bat`

```ps1
git switch dev :: переходим в dev
git merge --commit main  :: мерджим с main
git push :: отправляем на удаленный репозиторий
git switch stg :: повторяем для остальных 
git merge --commit dev 
git push
git switch prd
git merge --commit stg 
git push
@pause
```

`reset.bat`

```ps1
git clean -f :: удаляем все неиндексируемые файлы
git reset --hard :: отменяем все изменения и переводим HEAD на последую ревизию
```
