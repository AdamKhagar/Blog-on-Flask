# Blog

Flask is used as the framework in the project

The idea was to make a site similar to [habr](https://habr.com/). The goal of the project was to understand how websites work and to learn how to use Flask and etc.
By the way, this is my first big project and so don't be harsh :)

> __NOTE__: This project is not yet complete and some things (links, buttons, parts of the admin panel) do not work 

## Quick Start

> __NOTE__: The project uses Python 3.8, so need it installed first.

1. Intall `poetry`
2. `git clone git@github.com:AdamKhagar/blog.git`
3. Install requirements:   
`cd blog && poetry install`
4. Run :  
`poetry shell && python manage.py runserver`
5. You can also create an admin user:  
`python manage.py create_superuser -n John -l Smith -u admin -e admin@admin.com -p qwerty123`
