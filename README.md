# Лабораторная работа. Docker. Развёртывание JupyterHub
## 1. Подготовка:
* Прежде всего на соответствующем устройстве должен быть установлен Docker.
* Необходимо скачать файлы из папки репозитория ```/toBuild``` и разместить в любой директории устройства.
* В этой директории нужно создать папку ```/shared```[^1]. В неё можно положить все необходимые файлы, что должны быть импортированы в JupyterHub и доступны у всех пользователей.
[^1]: Можно изменить название директории импортируемых файлов, добавив в команду сборки образа следующий аргумент: ```--build-arg NOTEBOOKS_FROM=<название папки>```. По умолчанию: ```--build-arg NOTEBOOKS_FROM=/shared```.
## 2. Сборка образа и запуск:
* Откройте терминал в каталоге загруженных файлов и выполните команду:
```docker build -t juphub:main .```
* Далее начнётся сборка образа. Необходимо дождаться её окончания.
* После окончания сборки необходимо подготовить хранилище для постоянных данных будущего JupyterHub. Для этого выполните команду: ```docker volume create juphubdata```.
* После успешного создания хранилища можно на основе собранного образа создать контейнер. Выполните команду: ```docker run -d -v juphubdata:/home -p 80:8000 --name JupyterHub juphub:main```
* __P.S__: Можно изменить центральную директорию JupyterHub, добавив в команду сборки образа следующий аргумент: ```--build-arg HUB_PATH=<путь>```. По умолчанию: ```--build-arg HUB_PATH=/hub```.
## 3. Авторизация:
* После того, как получилось успешно запустить контейнер необходимо войти в JupyterHub. Для этого перейдите в браузере вашего устройства по адресу ```http://localhost:80/hub/login```
* Вы окажитесь на странице авторизации. Внизу окна авторизации будет ссылка: '__Sign up__ to create a new user'.
* Перейдите по этой ссылке. Вас перебросит на страницу создания аккаунта. Введите в следущие поля следующие данные:
  * Поле: __Username__, введите: ```admin```;
  * Поле: __Password__, введите: ```admin```;
  * Поле: __Confirm password__, введите: ```admin```;
* Нажмите кнопку __Create User__.
* Готово. Теперь вы создали аккаунт admin с паролем admin.
* Вернитесь на страницу авторизации. Введите данные от нового аккаунта администратора:
  * Поле: __Username__, введите: ```admin```;
  * Поле: __Password__, введите: ```admin```;
* Нажмите кнопку __Sign In__.
* Добро пожаловать в DockerHub!
## 4. Создание пользователей:
* Теперь если пользователи будут переходить на страницу создания аккаунта и регистрироваться, то просто так они войти не смогут. Администратору __admin__ необходимо будет перейти на страницу ```http://localhost:80/hub/authorize``` и подтвердить запрос на создание нового аккаунта.
# Как я пытался выполнить лабораторную работу:
1. Необходимо было найти способ установить сервис JupyterHub в контейнер и запустить его. Для этого я нашёл инструкцию JupyterHub на DockerHub'e: ```https://hub.docker.com/r/jupyterhub/jupyterhub/```. Как раз подошёл способ установки на ядро образа Python, ведь мы уже это отрабатывали на семинаре НИС'а.
2. Во время следования инструкции не всё шло гладко. Что-то не хотело запускаться. Приходилось гуглить ошибки и искать решение.
 2.1. Например, я пытался загрузить npm и nodejs на образе python...-alpine. Оказалось, что alpine слишком урезан. Пришлось перейти на bullseye.
 2.2. Скачать npm и nodejs не получалось. Оказалось, что нужно что-то докачать с сервера ```deb.nodesource.com``` с помощью curl. При попытке скачать npm после этого вылетала ошибка. Оказалось, что там npm уже присутствует.
3. Далее вроде всё нормально собиралось. Добавил всё необходимое в строку RUN: переброс порта контейнера, где работает JupyterHub на 8000, на локальный 80. Добавление хранения файлов /home за счёт VOLUME. Запустил. Теперь можно подключиться к JupyterHub'у. Зашёл, обрадовался, но авторизоваться не получалось.
4. Оказалось, что система авторизации JupyterHub очень навроченная и может быть реализована массой способов. Сначала я делал пользователя через adduser admin в терминале  контейнера. Но оказалось, что такой пользователь не имеет прав администратора. Потом я пытался через dummyauthenticator, но из-за него всё ломалось и не хотели запускаться notebook сервера для пользователей. Тогда я нашёл в одном видео решение в виде jupyterhub-nativeauthenticator. Для него ещё необходимо было сделать хук авторизации в конфиге. Я решил сделать так.
5. По поводу бонуса: вначале я думал, что

> при запуске контейнера/сборке образа Jupyter Hub загружать Jupyter Notebook из заданной директории...

означает, что нужно каким-то образом запускать сервер jupyter notebook. Однако позже это оказалось не так. Выходило, что нужно сделать так, чтобы у всех пользователей отображался некоторый <file>.ipynb. Я решил реализовать это так, чтобы у всех пользователей была доступна общая папка, в которой могут лежать любые файлы. Тогда во время docker build можно её перенести на JupyterHub и тем самым сделать возможным загрузить всем тот самый <file>.ipynb.
 5.1. Без проблем тут конечно тоже не обошлось. Можно было это реализовать клонированием файлов каждому пользователю, но я узнал, что в linux есть symlink, переадрессующая в некоторую папку. Также в JupyterHub предусмотрена возможность задавать нулевой образ notebook сервера пользователя (то есть то, что в нём должно изначально лежать у всех при создании). Тогда я решил в директорию /home переносить необходимую папку с <file>.ipynb. Делать в /etc/skel/ JypterHub'a symlink-ссылку на перенесённую папку. И тогда у всех она будет видна.
 5.2. Тут оказалось, что пользователи её не видят не смотря на то, что ссылка лежил в /etc/skel/ и должна у всех появляться. Решение нашёл в интернете. Оказалось, что у пользователей не хватает прав. Тогда я добавил команду на изменение прав папки, которая откроет доступ пользователям к содержимому и самой папке.
6. Тут уже всё работало как надо.
__P.S.__ Все файлы в репозиторий я перенёс где-то на этапе 4 и начал писать с этого момента README.md.
