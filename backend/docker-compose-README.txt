Setup: 
	- docker-compose up
Tear down:
	- docker-compose down --rmi all
		
		
What is going on:
1) Custom Kong Image (kong_nodb) is built that reads configuration from ./kong.yml instead of postgres DB as usual
2) Kong is deployed
3) MySQL DB is deployed
4) MySQL DB is filled up with data in ./mysql-init-files/init.sql
5) Book Image (From ./book) is built
6) Book Image is deployed but its port 5000 is ONLY exposed in kong-net bridge network

Since kong.yml points localhost:8000/book  -> book:5000, user can go to localhost:8000/book to call book:5000 endpoint