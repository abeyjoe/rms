Result Management System
(a case study of the department computer science, the polytechnic ibadan)
Python Programming Language

How to run the file

open the directory of where the file is located in terminal or CMD
type the following command:
python manage.py runserver

copy the server port and run it on a a browser

username: Admin
password: Admin2022
(Note: username & password are case sensitive)

How to mange the site from the admin page
type the following command:
1. python.exe manage.py migrate
2. python.exe manage.py migration
3. python.exe manage.py createsuperuser (to change the admin username)

Admin module to edit the site : "http://127.0.0.1:8000/admin"

After editing the source code, you need to migrate by typing the following commange:
python.exe manage.py migration