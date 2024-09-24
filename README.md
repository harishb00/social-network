* Install poetry
* `poetry install`
* `poetry shell`
* `cd src`
* `python manage.py runserver`


# Django commands
```
django-admin startproject django_project .
before first migration, setup the custom user model
python manage.py startapp accounts
implement CustomUser(django.contrib.auth.models.AbstractUser)
AUTH_USER_MODEL in `settings` file
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

# Questions
accounts/forms.py
why Meta class?
How to register a model in admin page?  https://docs.djangoproject.com/en/5.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin
what is fieldsets in django?
how each model fields work? eg: char with choices
Understand about models CASCADE feature
What does `related_name` attribute do in model definition
why setUpTestData method is a class method?


# how about duplicate entries in the model for friend request and blocked


# Misc
Thecomparisonoperator ∼=ensuresthat subsequent security updates for Django, such as 4.0.1,
 4.0.2, andsoonareautomaticallyinstalled.


# Docker
## Docker Image
A Docker image is a read-only template that describes how to create a Docker container. The
image is the instructions while the container is the actual running instance of an image. To
continue our apartment analogy from earlier in the chapter, an image is the blueprint or set
of plans for building an apartment; the container is the actual, fully-built building.

## Dockerfile
 To build our own image we create a special
 file known as a Dockerfile that defines the steps to create and run the custom image

## `.dockerignore`

`docker build .` builds the image. it uses the `Dockerfile` from current directory.

 In order to run the container
 weneed alist of instructions in a file called docker-compose.yml. 

 `docker-compose up` to run docker container

 What does WORKDIR actually mean? creating directory in container

 docker-compose exec web python manage.py createsuperuser
 docker-compose up 
 docker-compose up -d
 docker-compose down
 docker-compose up-d--build

  docker-compose exec web poetry run python manage.py migrate
 $ docker-compose exec web poetry python manage.py createsuperuser


 # TODO
 * Automate migrations during deployment

django-rest-auth


# References
https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0


https://dylancastillo.co/til/django-poetry-dockerfile.html

https://www.freecodecamp.org/news/how-to-use-jwt-and-django-rest-framework-to-get-tokens/

BEST:
https://medium.com/django-unleashed/securing-django-rest-apis-with-jwt-authentication-using-simple-jwt-a-step-by-step-guide-28efa84666fe [WORKING]
https://dev.to/ki3ani/implementing-jwt-authentication-and-user-profile-with-django-rest-api-part-3-3dh9
https://medium.com/django-rest/logout-django-rest-framework-eb1b53ac6d35
https://medium.com/@poorva59/implementing-simple-jwt-authentication-in-django-rest-framework-3e54212f14da
https://medium.com/django-unleashed/email-authentication-designing-a-modern-system-in-django-rest-framework-without-the-traditional-f2758ae08c31 [JWT Email auth]
