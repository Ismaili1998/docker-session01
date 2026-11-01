Session 01

Liste des commandes:

- construire une image => docker build -t <nom-image> .
- lister les images créées => docker images
- lancer un container => docker run --name <nom-container> <nom-image-créée>
- lister les conatiners créés => docker ps

To push an image to docker Hub

- docker tag my-image user_name/my-image:latest

- docker push user_name/my-image:latest

To pull an image:

- docker pull simox122/my-image1 (example de pull de l'image créée par simox122 user)

- pour runner un container à base de l'image pullé => docker run -it simox122/my-image1

session 02

Liste des commandes:

To run postgress container with env variables:

docker run --name postgres-container \
 -e POSTGRES_USER=postgres_user \
 -e POSTGRES_PASSWORD=root \
 -e POSTGRES_DB=db \
 -p 5432:5432 \
 -d postgres

To run python-app container with env variables:

docker run --name python-app-container \
 -e DB_USER=postgres_user \
 -e DB_PASSWORD=root \
 -e DB_NAME=db \
 -d python-app-image
