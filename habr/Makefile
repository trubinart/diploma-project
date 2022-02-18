start:
	sudo docker-compose up -d  --buil
	sudo docker-compose exec django python manage.py migrate
	sudo docker-compose exec django python manage.py collectstatic
	sudo docker-compose exec django python manage.py createsuperuser

up-start:
	sudo docker-compose up -d  --buil
	sudo docker-compose exec django python manage.py migrate

update:
	sudo docker-compose up -d  --buil

stop:
	docker-compose down -v

delete:
	docker system prune -a

postgre:
	docker-compose exec db psql --username=habr_admin --dbname=geek_habr_db

