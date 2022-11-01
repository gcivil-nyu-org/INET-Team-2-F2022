black .
flake8 .
coverage run --source=serenity_project/serenity_project,serenity_project/app serenity_project/manage.py test
coverage report 