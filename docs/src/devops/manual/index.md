# DevOps Documentation
<!-- Replace all of the titles with relevant titles -->

## Containers Used

### saeoss_ckan-web_1

This container is used to run the main application. All back end and front end logic can be found here. The ckan framework is installed in this container

### saeoss_ckan-background-worker_1

This container is used to create jobs that run in the 'background', i.e. asynchronously without blocking the main application

### saeoss_ckan-harvesting-fetcher_1

This container provides a common harvesting framework

### saeoss_ckan-harvesting-runner_1

This container provides the logic for running harvesting jobs

### saeoss_ckan-mail-sender_1

This container is used to send emails from the application

### saeoss_ckan-harvesting-gatherer_1

This container provides the logic for gathering data from harvester jobs

### saeoss_datastore-db_1

This container contains the database that used for the datastore

### saeoss_ckan-db_1

This container contains the database that used for the main application

### saeoss_redis_1

This container runs a redis server which is needed for ckan

### saeoss_datastore-test-db_1

This container contains the database that used to run tests for the datastore

### saeoss_ckan-test-db_1

This container contains the database that used to run tests for the main application

### saeoss_csw-harvest-target_1

This container provides the service to harvest data from a target specified

### saeoss_ckan-datapusher_1

This container provides a standalone web service that automatically downloads any tabular data files like CSV or Excel from the site's resources when they are added, parses them to pull out the actual data, then uses the DataStore API to push the data into the site's DataStore.

### saeoss_pycsw_1

This container runs a pycsw server which serves as an API to share data on the platform

### saeoss_solr_1

This container runs a solr server that is needed for ckan to index data and run spatial queries

## SDLC

*A systematic approach that generates a structure for the developer to design, create and deliver high-quality software based on customer requirements and needs. The primary goal of the SDLC process is to produce cost-efficient and high-quality products. The process comprises a detailed plan that describes how to develop, maintain, and replace the software.*

1. Identify the Current Problems 

This stage of the SDLC means getting input from all stakeholders, including customers, sales people, industry experts, and programmers. Learn the strengths and weaknesses of the current system with the goal of improvement.

2. Plan

In this stage of the SDLC, the team determines the costs and resources required for implementing the analyzed requirements. Also detailing the risks involved and providing sub-plans to mitigate those risks.

The team must determine the feasibility of the project and how they can successfully implement the project with the lowest risk in mind.

3. Design

This phase of the SDLC starts by turning the software specifications into a design plan called the Design Specification. All stakeholders then review this plan and offer feedback and suggestions. It’s crucial to have a plan for collecting and incorporating stakeholder input into this document. Failure at this stage will almost certainly result in cost overruns at best and the total collapse of the project at worst.

4. Build

At this stage, the actual development starts. It’s important that every developer sticks to the agreed blueprint. Also, make sure you have proper guidelines in place about the code style and practices.

For example, define a nomenclature for files or define a variable naming style such as camelCase. This will help your team to produce organized and consistent code that is easier to understand but also to test during the next phase.

5. Code Test

In this stage, we test for defects and deficiencies. We fix those issues until the product meets the original specifications.

In short, we want to verify if the code meets the defined requirements.

6. Software Deployment

At this stage, the goal is to deploy the software to the production environment so users can start using the product. However, many organizations choose to move the product through different deployment environments such as a testing or staging environment.

This allows any stakeholders to safely play with the product before releasing it to the market. Besides, this allows any final mistakes to be caught before releasing the product.

## Continuous Integration

*Continuous integration refers to the build and unit testing stages of the software release process. Every revision that is committed triggers an automated build and test*

## Testing Deployments

## Backend Orchestration

### Deployments

### Kubernetes
