db-up:
	sudo docker run --rm --name mysql -e MYSQL_ROOT_PASSWORD=password@123 -e MYSQL_DATABASE=auction -d -p 3306:3306 mysql:latest


db-down:
	sudo docker container stop mysql


db-reset:
	make db-down && make db-up

run:
	./serve.sh