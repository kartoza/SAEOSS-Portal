## General On SAEOSS Portal Services
SAEOSS is powered by several services spawned as docker containers - eventually deployed as kubernetes pods - 
the following are most notable ones:


### saeoss-ckan-web: 
This is the main repository for development code, it’s relies on Custom CKAN instance to perform metadata publishing 
functionalities (creation, validation ..etc.), it holds CLI Commands code, and code of several other services 
(harvesters, stac endpoints ..etc.)

### saeoss-ckan-db: 
This is the Database service, it uses Postgresql as a database engine and docker volumes to store relational data, once 
CKAN database is initialised, several standard tables are created automatically (package, resource, user, activity ..etc.).

### saeoss-solr: 
This service is based on apache solr8 which provides a search engine directed mainly towards saeoss-ckan-web, metadata 
records are requested through the portal (UI or CLI) and queries are constructed and sent to solr to return filtered sets.

### saoess-pycsw: 
This the main CSW service based on pycsw (https://pycsw.org/) python package, the services insures datasets are returned 
as an OGC standard results, the service also returns datasets as STAC items.  

### saeoss-ckan-mail-sender: 
A service responsible for sending aggregated mails to recipient users, site activities (creating datasets and publishing 
them, modifying datasets ..etc.) are stored in  saeoss-ckan-db and if relevant forwarded to users, in a production 
environment the main sender is called periodically with a cron-job and send stored mail in a given time-span 
(e.g the past two days), which activities to send mail for could be further customised.

### saeoss-ckan-harvesting-runner, saeoss-ckan-harvesting-fetcher, saeoss-ckan-harvesting-consumer: 
These three services are responsible for performing harvesting with CKAN, harvesting happens at four stages, once a 
harvesting source is provided (via the GUI or CLI), the runner is responsible for kicking-off pending harvesting jobs 
to the consumer (in a production environment the runner is called periodically via a cron job), the consumer compiles 
all the resource identifiers that need to be fetched and the fetcher gets the contents of the remote objects and 
stores them in the database, once the resources are brought in, new datasets would be created out of these resources.

### saeoss-redis:  
Redis is a famous key/value storage system used to cache request results to speed up web pages.

### saeoss-ckan-background-worker: 
The background worker holds the same configuration as the saeoss-ckan-web, as some processes would consume relatively 
more time to complete and consume more resources, the worker is meant to shorten time consumption with heavy tasks.
