---
title: SAEOSS Portal
summary: Discover a world of data-driven possibilities at the SAEOSS-Portal, where information converges to empower data sharing and decision-making.
    - Jeremy Prior
    - Juanique Voot
    - Ketan Bamniya
date: 28-03-2024
some_url: https://github.com/SANSA-EO/SAEOSS-PORTAL
copyright: Copyright 2024, SANSA
contact:
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
---

# Setting up your IDE

This section outlines the process for configuring your IDE (Integrated Development Environment) for development.

🚩 Make sure you have gone through the [Cloning Section](cloning.md) before following these notes.

## VS Code Setup

Open the project in VSCode (1️⃣, 2️⃣) by navigating the the place on your file system where you checked out the code in the pre-requisites step above (3️⃣).

![image.png](./img/ide-setup-1.png)

Accept the 'trust authors' prompt

![image.png](./img/ide-setup-2.png)

### Copying the .env

Copy the `template.env` to `.env`
![image.png](./img/ide-setup-3.png)
Edit the `.env` file and change the

```
DJANGO_SETTINGS_MODULE=core.settings.prod
```
to   

```
DJANGO_SETTINGS_MODULE=core.settings.dev
```

[![image.png](./img/ide-setup-4.png)](./img/ide-setup-1.png)

### Override Docker Configs

We are going to copy the docker overrides template to a local file that will not be under version control.

[![image.png](./img/ide-setup-5.png)](./img/ide-setup-5.png)

Rename the file to `docker-compose.override.yml`

[![image.png](./img/ide-setup-6.png)](./img/ide-setup-6.png)

Initially you will not need to change anything in this file, though you may want to take a look through the various configurations provided here if you want to tweak your local setup.

Now that you have your IDE set up, we can move on to [building the project](building.md).

## Using pycharm

This section is for using pycharm.

Requirements:

- Pycharm
- Finished **Setting up the project**

## Setup interpreter

1. Go to file -> setting -> Project -> Project Interpreter -> click cog -> add
   <br>![Project Interpreter ](img/1.png "Project Interpreter")<br><br>

2. Go to ssh interpreter -> Fill the form like below
   <br>![Project Interpreter ](img/2.png "Project Interpreter")<br><br>

3. Click next and fill **docker** as password
   <br>![Project Interpreter ](img/3.png "Project Interpreter")<br><br>

4. Click next and change interpreter like below and click finish
   <br>![Project Interpreter ](img/4.png "Project Interpreter")<br><br>

5. After finish, it will show all package like below.
   <br>![Project Interpreter ](img/5.png "Project Interpreter")<br><br>

6. In current page, click **path mappings**, click + button and put local path to where the project (django-project folder) and remote path is like below. and click oK.
   <br>![Project Interpreter ](img/6.png "Project Interpreter")

Now the interpreter is done. When we restart the machine, we need to do `make up` to run the project.

## Setup run configuration

After the interpreter is done, we need configuration to run the project in development mode.

1. Click "Add configuration" like in the cursor in the image below. (top-right)
   <br>![Project Interpreter ](img/7.png "Project Interpreter")<br><br>

2. There will be a popup, and click +, then click **django server** like below
   <br>![Project Interpreter ](img/8.png "Project Interpreter")
   <br>![Project Interpreter ](img/9.png "Project Interpreter")<br><br>

3. It will show the form and fill like below.
   <br>![Project Interpreter ](img/10.png "Project Interpreter")<br><br>

4. Don't click the OK yet, but click **Environment Variables** and add environments like below 9by clicking + button).
   <br>![Project Interpreter ](img/11.png "Project Interpreter")<br><br>

5. After that, click OK.

6. Now we need to run the server by clicking **go** button in below image.
   <br>![Project Interpreter ](img/12.png "Project Interpreter")<br><br>

7. When we click the **go** button, pycharm will run a process until like image below.
   <br>![Project Interpreter ](img/13.png "Project Interpreter")<br><br>

8. Now it is done. We can access the development server in [http://localhost:2000/](http://localhost:2000/)

This development mode is DEBUG mode, and also whenever we change the code, the site will also change in runtime.

For more information how to set up on pycharm, please visit [Using a Docker Compose-Based Python Interpreter in PyCharm](https://kartoza.com/en/blog/using-docker-compose-based-python-interpreter-in-)

---------------------------------

## Quick Installation Guide

This project is a [ckan](https://ckan.org/) extension, it can be installed standalone. To deploy this project we use  [docker,](http://docker.com/) so you need to have docker running on the host.

> **NOTE:** *Docker is needed to continue with the quick installation guide. Ensure you have docker installed on your system before continuing.*

Build docker images

```bash
cd SAEOSS-Portal/docker
./build.sh
```

Start up project

```bash
./compose.py --compose-file docker-compose.yml --compose-file docker-compose.dev.yml up
```

Run down the project

```bash
./compose.py --compose-file docker-compose.yml --compose-file docker-compose.dev.yml down
```

After starting up, the project is available on your local host at http://localhost:5000 

### Operations

#### Rebuild solr index

```bash
# check if there are any datasets that are not indexed
ckan search-index check

# re-index
docker exec -it saeoss_ckan_web_1 poetry run ckan search-index rebuild
```

#### Operate harvesters

You may use the various `ckan harvester <command>` commands to operate existing harvesters.

Create a job:

```bash
docker exec -t saeoss-ckan_harvesting-runner poetry run ckan harvester job <source-id>
```

#### Send notifications by email

This needs to be run periodically (once per hour is likely enough).

```bash
docker exec -it saeoss_ckan_web_1 ckan saeoss send-email-notifications
```

Additionally, in order for notifications to work, there is some configuration:

- The CKAN settings must have `ckan.activity_streams_email_notifications = true`
- The CKAN settings must have the relevant email configuration (likely being passed
  as environment variables)
- Each user must manually choose to receive notification e-mails - This is done in
  the user's profile
- Each user must manually follow those entities (datasets, organizations, etc) that
  it finds interesting enough in order to be notified of changes via email

#### Refresh pycsw materialized view

This needs to be run periodically (once per hour is likely enough).

```bash
docker exec -t ckan dalrrd-emc-dcpr pycsw refresh-materialized-view
```

#### Create sysadmin user

After having initialized the database you can now create the first CKAN
sysadmin user.

```bash
docker exec -ti saeoss_ckan_web_1 poetry run ckan sysadmin add admin
```

Answer the prompts in order to provide the details for this new user.
After its successful creation you can login to the CKAN site with the `admin`
user.

#### Initialize CKAN database

The first time you launch it you will need to set up the ckan database (since
the ckan image's entrypoint explicitly does not take care of this, as
mentioned above). Run the following command:

```bash
docker exec -ti saeoss_ckan_web_1 poetry run ckan db init
```

Afterwards, proceed to run any migrations required by the ckanext-dlarrd-emc-dcpr extension

```bash
docker exec -ti saeoss_ckan_web_1 poetry run ckan db upgrade --plugin dalrrd_emc_dcpr
```

Now you should be able to go to `http://localhost:5000` and see the ckan
landing page. If not, you may need to reload the ckan web app after
performing the DB initialization step. This can done by sending the `HUP`
signal to the gunicorn application server (which is running our ckan
flask app):

```bash
docker exec -ti saeoss_ckan_web_1 bash -c 'kill -HUP 1'
```

#### Generate pycsw DB view

In order to be able to serve the system's datasets through various OGC standards, create a DB materialized view
in order to integrate with pycsw:

```bash
docker exec -ti saeoss_ckan_web_1 poetry run ckan dalrrd-emc-dcpr pycsw create-materialized-view
```

#### Ingest a collection of metadata from a given directory (currently CBERS xml files)

create datasets (metadata records) from files stored in a directory

```bash
docker exec -ti saeoss_ckan_web_1 poetry run ckan saeoss ingest cbers --source-path <path> --user <username>
```

#### Perform STAC Fetch and create datasets from STAC endpoint  

create datasets (metadata records) from stac endpoint

```bash
docker exec -ti saeoss_ckan_web_1 poetry run ckan saeoss stac create-stac-dataset --url <url> --user <username> --max <max_number_of_records>
```

---------------------------------

### Production

Section for juanique and zakki to complete
<!-- 
```
git clone https://github.com/kartoza/SAEOSS-Portal
cd SAEOSS-Portal/docker
docker-compose up -d
```

The web will be available at [http://localhost:5000](http://localhost:5000)

To stop containers:

```
docker-compose kill
```

To stop and delete containers:

```
docker-compose down
``` -->

### Development

Section for juanique and zakki to complete

<!-- ```
git clone https://github.com/kartoza/SAEOSS-Portal
cd SAEOSS-Portal/docker
cp .template.env .env
cp docker-compose.override.template.yml docker-compose.override.yml
```

After that, do
- open new terminal
- on folder root of project, do
```
make frontend-dev
```
Wait until it is done
when there is sentence "webpack xxx compiled successfully in xxx ms".<br>
After that, don't close the terminal.
If it is accidentally closed, do `make frontend-dev` again

Next step:
- Open new terminal
- Do commands below
```
make up
make dev
```

Wait until it is on.

The web can be accessed using `http://localhost:2000/`

If the web is taking long time to load, restart geosight_dev container by `make dev-reload`.<br>
The sequence should be `make frontend-dev`, after that run or restart geosight_dev. 

To stop dev:

```
make dev-kill
```

To reload container:

```
make dev-reload
``` -->
