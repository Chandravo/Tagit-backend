set -o errexit  # exit on error

cd config

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate