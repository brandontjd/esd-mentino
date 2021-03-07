Setup: 
	- docker-compose up
Tear down:
	- docker-compose down --rmi all
		
		
What is going on:
1) Custom Kong Image (kong_nodb) is built that reads configuration from ./kong.yml instead of postgres DB as usual
2) Kong is deployed
3) MySQL DB is deployed
4) MySQL DB is filled up with data in ./mysql-init-files/init.sql
5) User Image (From ./User) is built
6) User Image is deployed but its port 5004 is ONLY exposed in kong-net bridge network

kong.yml points localhost:8000/user  -> user:5004/user