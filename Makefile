.PHONY: migrate, run

dump:
	DJANGO_SETTINGS_MODULE='core.settings' django-admin dumpdata --all --indent 4 -o dump.json

migrate:
	python manage.py makemigrations
	python manage.py migrate

run:
	python manage.py runserver

collectstatic:
	python manage.py collectstatic
