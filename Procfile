web: python manage.py migrate --noinput && python copy_and_seed_data.py && python manage.py collectstatic --noinput && gunicorn fit_and_fine.wsgi:application
