# SAEOSS-Portal
The SAEOSS Portal has been proposed as a system of software components functioning together as the national central earth observation geospatial repository, with a view to metadata and open geospatial API standards compliance as well as user impact maximization 


# Deployment
This project is deployed onto following environment:

- Testing: TBD
- Staging: TBD
- Production: TBD

# Quick Installation Guide
This project is a [ckan](https://ckan.org/) extension, it can be installed standalone. To deploy this project we use  [docker,](http://docker.com/) so you need to have docker running on the host.

Clone the source cose
```
git clone git@github.com:kartoza/SAEOSS-Portal.git
```

Build docker images

```
cd SAEOSS-Portal/docker
./build.sh
```

Run and down the project

```
./compose.py --compose-file docker-compose.yml --compose-file docker-compose.dev.yml up
./compose.py --compose-file docker-compose.yml --compose-file docker-compose.dev.yml down
```

After running, the project is available on your local host at http://localhost:5000 