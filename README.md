# Foodgram
![workflow status](https://github.com/IuriyLeb/foodgram-project-react/actions/workflows/main.yml/badge.svg)

Foodgram is a service for creating recipes.

Users can create recipes, add it to favorites and in shopping cart.

Also, users can subscribe to another users.


## Installation

Use the [DockerHub](https://hub.docker.com/) to download foodgram image.

```bash
docker pull ileeb/foodgram
```
After download, you need to run image and set enviromental variables
```
docker run --env-file [.env file] ileeb/foodgram
```
Then, make migrations, create superuser and collect static
```bash
docker-compose exec web python manage.py migrate
```
```bash
docker-compose exec web python manage.py createsuperuser
```
```bash
docker-compose exec web python manage.py collectstatic --no-input 
```

After all, the Foodgram project will be available in [localhost/](http://localhost/)
## Usage

Foodgram has pretty good documentation, built on ReDoc. You can access it on [localhost/api/docs/](http://localhost/api/docs/)

## More
### .env file structure
```dosini
DB_ENGINE
DB_NAME
POSTGRES_USER
POSTGRES_PASSWORD
DB_HOST
DB_PORT
SECRET_KEY
```

### About us
Author: [Lebeda Iuriy](https://github.com/IuriyLeb)

This project was done as a part of learning in [Yandex.Practicum](https://practicum.yandex.ru/) courses.

If you have any suggestions/comments, open pull requests or contact me by email.

### Contributing
Project is available in : [http://51.250.16.204/](http://51.250.16.204/)



Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

### License
[MIT](https://choosealicense.com/licenses/mit/)
