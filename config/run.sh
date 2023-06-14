python manage.py migrate
python manage.py collectstatic --noinput
daphne -e ssl:4376:privateKey=privkey.pem:certKey=cert.pem config.asgi:application
