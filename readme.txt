Условие задачи:
https://greentask.in/zgrgxez

Задача реализована частично. С Twitter bootstrap на момент выполнения тестового задания не знаком, равно как и не знаю, для каких конкретно процессов необходимо написать unit-тесты.


Код выложен на GIT-репозиторий. Что касается инструкции по развертыванию, она прилагается ниже.


ИНСТРУКЦИЯ ПО РАЗВЕРТЫВАНИЮ

Условия:
Linux-сервер с предустановленным Python3 и pip.
Подключенный домен, то 
Предполагается, что проект уже загружен по адресу /home/ИМЯ_ПОЛЬЗОВАТЕЛЯ/webapps/company_base (в company_base лежат файлы и директории уровня manage.py).

ШАГИ

1) Скачиваем virtualenv и другие пакеты для проекта:
sudo pip install virtualenv
cd /home/ИМЯ_ПОЛЬЗОВАТЕЛЯ/virtenvs
virtualenv company_env --python=python3
pip install -r /home/ИМЯ_ПОЛЬЗОВАТЕЛЯ/webapps/company_base/requirements.txt
sudo apt-get install nginx
sudo /etc/init.d/nginx start

2) Создаем файл uwsgi_params на одном уровне с manage.py со следующим содержанием:
https://github.com/nginx/nginx/blob/master/conf/uwsgi_params

3) Создаем ссылку от уже подготовленного файла company_nginx.conf (на одном уровне с manage.py) в /etc/nginx/sites-enabled:
sudo ln -s /home/ИМЯ_ПОЛЬЗОВАТЕЛЯ/webapps/company_base/company_nginx.conf /etc/nginx/sites-enabled

Примечание: в файле настроек есть следующая строка:
server_name     yourserver.com;
Вместо yourserver.com впишите домен, к которому привязываете проект.

Перезагружаем nginx:
sudo /etc/init.d/nginx restart

5) Тестируем, видит ли nginx медиа и статику.
В папку /home/ИМЯ_ПОЛЬЗОВАТЕЛЯ/webapps/company_base/media (папку media надо будет создать) перенесите любое изображение (допустим, с названием, filler.png). Вбейте в адресную строку:
http://127.0.0.1:8000/media/filler.png
Теперь тестируем статику:
http://127.0.0.1:8000/static/css/styles.css

6) Устанавливаем uwsgi глобально
sudo pip3 install uwsgi
Вбиваем команду (вы должны быть в /home/ИМЯ_ПОЛЬЗОВАТЕЛЯ/webapps/company_base):
uwsgi --socket company.sock --module company_base.wsgi --chmod-socket=666

После этого вы должны увидеть полноценно работающий проект. Едем дальше.

6) Деактивируем виртуальное окружение командой:
deactivate

Ставим uwsgi глобально:
sudo pip3 install uwsgi

Теперь для запуска достаточно в корне проекта прописывать следующее:
uwsgi --ini company_uwsgi.ini
Попробовали?

Создаем папку для конфигурационных файлов:
sudo mkdir /etc/uwsgi
sudo mkdir /etc/uwsgi/vassals

Создаем ссылку на company_uwsgi.ini:
sudo ln -s /home/ИМЯ_ПОЛЬЗОВАТЕЛЯ/webapps/company_base/company_uwsgi.ini /etc/uwsgi/vassals/

Запускаем проект следующей командой
sudo uwsgi --emperor /etc/uwsgi/vassals --uid UID_ПОЛЬЗОВАТЕЛЯ --gid GID_ПОЛЬЗОВАТЕЛЯ

В файл /etc/rc.local перед строкой “exit 0” добавляем:
/usr/local/bin/uwsgi --emperor /etc/uwsgi/vassals --uid UID_ПОЛЬЗОВАТЕЛЯ --gid GID_ПОЛЬЗОВАТЕЛЯ


Все, вводим sudo reboot и смотрим, как наш сайт автоматически запускается после перезагрузки сервера.
