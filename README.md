# Trip-Tickets-Web
+ Run MySQL environment use Docker.
```shell
$ docker run --name=local-mysql5.7 -p 3306:3306 -e MYSQL_ROOT_PASSWORD=*** -e MYSQL_DATABASE=trip-ticketsDB -d mysql:5.7
```
+ Login MySQL
```shell
$ docker exec -it local-mysql5.7 mysql -uroot -p
```
