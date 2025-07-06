run:
	poetry run python manage.py runserver

migrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate

superuser:
	poetry run python manage.py createsuperuser

shell:
	poetry run python manage.py shell

activate:
	poetry shell