# nginx_start_py
Nginx start service from my PC windows to Centos 6.10

#Step logic script:
#
#
Логика работы скрипта:
1. Подключаемся к серверу
1.1 Если нет, выдаем ошибку
2. Запускаем nginx, ждем ответ после запуска команды
3. Проверяем циклом, если страница отдает 200ОК, то перезодим к п.4
3.1 Если страница отдает какой либо номер статуса, то грузим правильный default.conf, перезапускаем service nginx
3.2 Если приходит ответ, что страница не существует, то грузим правильный default.conf, перезапускаем service nginx
4. Грузим файл index.html, ждем 2 сек., пишем, что можно работать, закрываем SSH сессию.
#
