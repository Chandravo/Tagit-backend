python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
daphne -e ssl:4376:privateKey=privkey.pem:certKey=cert.pem config.asgi:application
