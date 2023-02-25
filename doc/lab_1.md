# ЛР 1\#: [C++ & UNIX]: UNIX знакомство: useradd, nano, chmod, docker, GIT, CI, CD #

Карсаков Григорий Вячеславович, 3 курс (ФизФ ИТМО), Z33434, 2023

## Цель ##
Познакомить студента с основами администрирования программных комплексов в ОС семейства UNIX, продемонстрировать особенности виртуализации и контейнеризации, продемонстрировать преимущества использования систем контроля версий (на примере GIT)

## Решение ##

1.  [ОС] Работа в ОС, использование файловой системы, прав доступа, исполение файлов
    1.	В папке /USR/LOCAL/ создать 2 директории: folder_max, folder_min
    
    ```bash 
    root@user:~# cd /usr/local
    root@user: /usr/local# mkdir folder_max folder_min


    root@user: /usr/local# ls
    bin etc foldef_max folder_min games incluse lib man sbin shere src
    
    ```

    2.	Создать 2-х группы пользователей: group_max, group_min
    
    ```bash 
    root@user:~# groupadd group_max
    root@user:~# groupadd group_min


    root@user:~# getent group
    ...
    group_max
    group_min
    ...
    ```
    
    3.	Создать 2-х пользователей: user_max_1, user_min_1
    ```bash 
    root@user:/usr/local# useradd user_max_1
    root@user:/usr/local# useradd user_min_1


    root@user:/usr/local# usermod -a -G group_max user_max_1
    root@user:/usr/local# usermod -a -G group_min user_min_1


    root@user:/usr/local# members group_max
    user_max_1
    root@user:/usr/local# members group_min
    user_min_1
    
    ```

    4.	Для пользователей из группы *_max дать полный доступ на директории *_max и *_min. Для пользователей группы *_min дать полный доступ только на директорию *_min
    ```bash 
    root@user:/usr/local# chmod a=rwx folder_min
    root@user:/usr/local# chmod o-w folder_max
    root@user:/usr/local# chmod o-w folder_max

    root@user:/usr/local# getfacl folder_max
    # file: folder_max
    # owner: root
    # group: group_max
    user::rwx
    group::rwx
    other::r-x
    ```

    5.	Создать и исполнить (пользователем из той же категории) скрипт в директории folder_max, который пишет текущую дату/время в файл output.log в текущей директории
    ```bash 
    #!bin/bash/
    echo "date is $(date '+%d-%m-%Y-%H-%M-%S')" >> output.log
    
    $ whoami
    user_max_1
    $ pwd
    /usr/local/folder_max 
    $ ./date.sh
    $ ls
    date.sh  output.log
    ```


    6.	Создать и исполнить (пользователем из той же категории) скрипт в директории folder_max, который пишет текущую дату/время в файл output.log в директории *_min
    ```bash 
    #!bin/bash/
    echo "date is $(date '+%d-%m-%Y-%H-%M-%S')" >> /usr/local/folder_min/output_from_max.log
    $ whoami
    user_max_1
    $ pwd
    /usr/local/folder_max 

    $ bash date_in_min.sh


    $ cd ..
    $ cd folder_min
    $ ls
    outpt_from_max.log
    ```


    7.	Исполнить (пользователем *_min) скрипт в директории folder_max, который пишет текущую дату/время в файл output.log в директории *_min
    ```bash 
    $ whoami
    user_min_1
    $ pwd
    /usr/local/folder_max 

    $ bash date_in_min.sh

    $ bash date_in_min.sh
    $ cd ..
    $ cd folder_min 
    $ ls
    date.sh  output_from_max.log
    ```


    8.	Создать и исполнить (пользователем из той же категории) скрипт в директории folder_min, который пишет текущую дату/время в файл output.log в директории *_max
    ```bash 
    $ whoami
    user_min_1
    $ pwd
    /usr/local/folder_min

    $ bash date_in_max.sh

    $ cd ..
    $ cd folder_max
    $ nano output.log
    %% date is 23-02-2023-15-16-04
    %% date from min is 23-02-2023-16-31-33
    ```


    9.	Вывести перечень прав доступа у папок *_min/ *_max, а также у всего содержимого внутри
    ```bash 
    $ ls -l
    total 40
    ...
    drwxrwxr-x 2 user_max_1 group_max 4096 фев 23 16:28 folder_max
    drwxrwxrwx 2 user_min_1 group_max 4096 фев 23 16:31 folder_min
    ...
    $ cd folder_max
    $ ls -l
    total 12
    -rwxrwxr-x 1 user_max_1 user_max_1 101 фев 23 15:22 date_in_min.sh
    -rwxrwxr-x 1 user_max_1 user_max_1  71 фев 23 14:57 date.sh
    -rw-rw-rwx 1 user_max_1 user_max_1  65 фев 23 16:31 output.log
    $ cd ..
    $ cd folder_min
    $ ls -l
    total 12
    -rwxrwxr-x 1 user_min_1 user_min_1 101 фев 23 16:31 date_in_max.sh
    -rwxrwxrwx 1 user_min_1 user_min_1  16 фев 23 15:30 date.sh
    -rwxrwxrwx 1 user_max_1 user_max_1  84 фев 23 16:13 output_from_max.log
    ```

2. [КОНТЕЙНЕР] docker build / run / ps / images

    1.	Создать скрипт, который пишет текущую дату/время в файл output.log в текущей директории
    ```bash 
    touch Dockerfile
    nano Dockerfile
    FROM ubuntu:20.04
    RUN apt update && apt install nano && apt install bash
    ADD date.sh .
    ```

    2.	Собрать образ со скриптами выше и с пакетом nano (docker build)
    ```bash 
    docker build -t myubuntu .

    root@user:/usr/local/# docker ps
    CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
    d17c9a0d1224 myubuntu "/bin/bash" 22 hours ago Up 22 hours adoring_brown
    ```

    3.	Запустить образ (docker run)
    ```bash 
    docker run -it myubuntu
    ```

    4.	Выполнить скрипт, который подложили при сборке образа
    ```bash 
    root@d17c9a0d1224:/# ls
    bin  boot  date.sh  dev  etc  home  lib  lib32  lib64  libx32  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
    root@d17c9a0d1224:/# ./date.sh


    root@d17c9a0d1224:/# ls
    bin  boot  date.sh  dev  etc  home  lib  lib32  lib64  libx32  media  mnt  opt  output.log  proc  root  run  sbin  srv  sys  tmp  usr  var
    ```

    5.	Вывести список пользователей в собранном образе
    ```bash 
    root@user:/usr/local/folder_max# docker run myubuntu id
    uid=0(root) gid=0(root) groups=0(root)
    ```

3.  [GIT] GitHub / GitLab, в котором будут содержаться все выполненные ЛР
    1.	Создать репозиторий в GitHub или GitLab
    ```bash 
    root@user:/usr/local# apt install git
    ...
    root@user:/usr/local# git config --global user.name SpongeFrogy
    root@user:/usr/local# git config --global user.email droidb1poc@gmail.com
    root@user:/usr/local# git remote set-url origin https://TOKEN FROM      SITE@github.com/SpongeFrogy/6sem_Cpp_and_unix.git/
    ```
    2.	Создать структуру репозитория 
    ```bash 
    root@user:/usr/local# git add folder_max
    root@user:/usr/local# git add folder_min
    root@user:/usr/local# git push -u origin main

    %% создаем фиктивную ветку
    root@user:/usr/local# git branch fix
    root@user:/usr/local# git push -u origin fix
    ```
    3.	Создать ветки dev / stg / prd, удалить ранее существующие ветки удаленно и локально

    ```bash 
    root@user:/usr/local# git branch dev
    root@user:/usr/local# git branch stg
    root@user:/usr/local# git branch prd
    root@user:/usr/local# git push -u origin dev
    root@user:/usr/local# git push -u origin stg
    root@user:/usr/local# git push -u origin prd

    root@user:/usr/local# git push origin :fix
    To https://github.com/SpongeFrogy/6sem_Cpp_and_unix.git/
     - [deleted]         fix
    ```
    4.  Создать скрипт автоматического переноса ревизий из ветки dev в ветку stg с установкой метки времени (tag). Скрипт в корень репозитория
    ```bash
    #!/bin/bash
    VAR=$(date '+%d.%m.%Y.%H.%M.%S')
    git checkout stg
    git merge --commit dev 
    git tag "$VAR"
    git push origin stg
    git push origin "$VAR"
    ```
    5.  Создать скрипт автоматического переноса ревизий из ветки stg в ветку prd с установкой метки времени (tag). Скрипт в корень репозитория
    ```bash
    #!/bin/bash
    VAR=$(date '+%d.%m.%Y.%H.%M.%S')
    git checkout prd
    git merge --commit stg
    git tag "$VAR"
    git push origin prd
    git push origin "$VAR"
    ```
## Заключение ##
По итогу я научился определять права в системе Linux у пользователей и групп пользователей, научились работать с системой docker и GIT

## Вопросы по защите 25.02 ##

### Про GIT: В чем разница между push и pull? ###

Команда `git push` позволяет отправлять локальную ветку на удаленный репозиторий. Она помогает разработчикам синхронизироваться в команде, а именно отправляет проделанные изменения. Если программист работает один, то пуш позволяет хранить код в облаке gitlab и не только, избавляя от риска потери данных на компьютере.

Дополнительно для синхронизации еще используют `git pull` для получения изменений с сервера, чтобы получить список удаленных подключений к репозиторию.

[взято тут](https://selectel.ru/blog/tutorials/what-is-git-push-and-how-to-use-it/)

### Про разницу между VBox и Docker ###

Как уже было сказано, изначально виртуальная машина инициируется с фиксированным объём памяти и задействованных ядер, которые в конкретный момент могут не использоваться, что ведет к наличию зарезервированных, но не используемых мощностей. Докер инициируется с точно необходимым объемом памяти и ядер, а после выполнения их освобождает, рационально используя мощности сервера. 

Также, если смотреть глубже, разница между виртуализацией и контейнеризацей в уровнях инициации: ВМ начинается с нижнего уровня ОС (уровня ядра ОС), позволяя определять параметры работы ядра, тогда как контейнер находится на среднем уровне ОС, т.е. ОС выделяет системные ресурсы для работы контейнера. Именно поэтому важно, чтобы ОС машины и ОС контейнера совпадали.




