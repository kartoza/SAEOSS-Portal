

# Project Setup

## Clone SAEOSS-Portal repository

This will clone the SAEOSS-Portal repository to your machine
```
git clone https://github.com/kartoza/SAEOSS-Portal.git
```

## Project Setup

### Docker installation

The project needs docker to be able to run it. To install it, please follow below instruction.

```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg     
```

On the next prompt line:

```
echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg]https:download.docker.com/linux/ubuntu \
$(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

Run apt update:

```
sudo apt-get update
```

This will install docker
```
sudo apt-get install  docker-ce-cli containerd.io
```

This will check if installation of docker was successful
```
sudo docker version
```
And it should return like this

```
Client: Docker Engine - Community
 Version:           20.10.9
 API version:       1.41
 Go version:        go1.16.8
 Git commit:        c2ea9bc
 Built:             Mon Oct  4 16:08:29 2021
 OS/Arch:           linux/amd64
 Context:           default
 Experimental:      true

```

### Manage docker as non-root

This will ensure that the docker can be executed without sudo.
```
sudo systemctl daemon-reload
sudo systemctl start docker
sudo usermod -a -G $USER
sudo systemctl enable docker
```

Verify that you can run docker commands without sudo.
```
docker run hello-world
```

For more information how to install docker, please visit [Install Docker Engine](https://docs.docker.com/engine/install/)

### Get the project up and running

1. Navigate to docker folder `cd SAEOSS-Portal/docker`
2. Run the script to build the docker containers `./build.sh`
3. Start the containers `./compose.py --compose-file docker-compose.yml --compose-file docker-compose.dev.yml up`
4. The first time you launch it you will need to set up the ckan database (since the ckan image's entrypoint explicitly does not take care of this). Run the following command: `docker exec -ti saeoss_ckan-web_1 poetry run ckan db init`
5. Afterwards, proceed to run any migrations required by the ckanext-saeoss extension `docker exec -ti saeoss_ckan-web_1 poetry run ckan db upgrade --plugin saeoss`
6. After having initialized the database you can now create the first CKAN sysadmin user `docker exec -ti saeoss_ckan-web_1 poetry run ckan sysadmin add admin`. Answer the prompts in order to provide the details for this new user. After its successful creation you can login to the CKAN site with the admin user.
7. In order to be able to serve the system's datasets through various OGC standards, create a DB materialized view in order to integrate with pycsw: `docker exec -ti saeoss_ckan-web_1 poetry run ckan dalrrd-emc-dcpr pycsw create-materialized-view`
8. Rebuild solr index: `docker exec -it saeoss_ckan-web_1 poetry run ckan search-index rebuild`
9. You can access the site on your localhost by visting [http:localhost:5000](http:localhost:5000)


