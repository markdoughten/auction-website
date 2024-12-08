db-up:
	sudo docker run --rm --name mysql -e MYSQL_ROOT_PASSWORD=password@123 -e MYSQL_DATABASE=auction -d -p 3306:3306 mysql:latest


db-down:
	sudo docker container stop mysql


db-reset:
	make db-down && sleep 1 && make db-up




db-seed:
	curl "http://localhost:5000/seed/users" -X "POST" && \
	curl "http://localhost:5000/seed/item_meta" -X "POST" && \
	curl "http://localhost:5000/seed/items" -X "POST" && \
	curl "http://localhost:5000/seed/auctions" -X "POST" && \
	curl "http://localhost:5000/seed/bids" -X "POST" 



run:
	./serve.sh

reset:
	make db-reset && sleep 3 && ./serve.sh

