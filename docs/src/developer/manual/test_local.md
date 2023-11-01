# SCRUM Board

Testing uses some additional configuration:

- The `docker/docker-compose.dev.yml` file has an additional `ckan-test-db` service, with a DB that is uses solely
  for automated testing.
- The  `docker/ckan-test-settings.ini` file defines the test settings. It must be explicitly passed as the config
  file to use when running the tests

To run the tests you will need to:

1. Install the development dependencies beforehand, as the docker images do not have them. Run:

   ```
   docker exec -ti {container-name} poetry install
   ```

2. Initialize the db - this is only needed the first time (the dev stack uses volumes to persist the DB)

   ```
   docker exec -ti saeoss-ckan-web-1 poetry run ckan --config docker/ckan-test-settings.ini db init
   docker exec -ti saeoss-ckan-web-1 poetry run ckan --config docker/ckan-test-settings.ini harvester initdb
   docker exec -ti saeoss-ckan-web-1 poetry run ckan --config docker/ckan-test-settings.ini db upgrade -p saeoss
   ```

3. When there are model changes you will need to upgrade the DB too. Run this:

   ```
   docker exec -ti saeoss-ckan-web-1 poetry run ckan --config docker/ckan-test-settings.ini db upgrade -p saeoss
   ```

4. Run the tests with `pytest`. We use markers to differentiate between unit and integration tests. Run them like this:

   ```
   # run all tests
   docker exec -ti saeoss-ckan-web-1 poetry run pytest --ckan-ini docker/ckan-test-settings.ini

   # run only unit tests
   docker exec -ti saeoss-ckan-web-1 poetry run pytest --ckan-ini docker/ckan-test-settings.ini -m unit

   # run only integration tests
   docker exec -ti saeoss-ckan-web-1 poetry run pytest --ckan-ini docker/ckan-test-settings.ini -m integration
   ```