db-up:
	sudo docker run --rm --name mysql -e MYSQL_ROOT_PASSWORD=password@123 -d -p 3306:3306 mysql:latest


db-down:
	sudo docker container stop mysql


db-reset:
	make db-down && sleep 1 && make db-up




db-seed:
	curl "http://localhost:5000/seed/all" -X "POST"


run:
	./serve.sh

reset:
	make db-reset && sleep 3 && ./serve.sh

