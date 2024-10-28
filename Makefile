

build:
	docker-compose build

env.default:
	test -f .env || cp -v .env.example .env

up:
	docker-compose up --detach --build

down:
	docker-compose down

downv:
	docker-compose down --volumes

test:
	docker-compose exec apidrf python manage.py test

fmt:
	docker-compose exec apidrf black .

fmt.check:
	docker-compose exec apidrf black --check .

coverage:
	docker-compose exec apidrf coverage run --source='.' manage.py test
	docker-compose exec apidrf coverage report
	docker-compose exec apidrf coverage html
	docker-compose exec apidrf coverage xml
