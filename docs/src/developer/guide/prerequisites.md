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

# Project Prerequisites

## Installation of Docker

Ensure that Docker is installed on the machine where the environment will be set up using Docker Compose.
Follow the official Docker installation guide for your operating system to install Docker: [Docker Installation Guide](https://docs.docker.com/engine/install/).

## Minimal Dependencies Outside Docker

Since the environment is set up using Docker Compose, there are minimal dependencies outside Docker itself.
Docker Compose will handle the setup and orchestration of containers, so there's no need for additional software or dependencies.

## Configuration in Docker Compose

Define the services and configurations needed for the environment in the docker-compose.yml file.
Specify any required Docker images, volumes, networks, ports, environment variables, and other settings in the Docker Compose configuration.

## Sudo Rights for Docker

Ensure that the user running Docker commands has sudo rights to execute Docker commands without requiring a password.
Granting sudo rights to Docker commands can be done by adding the user to the Docker group. However, it's essential to understand the security implications of this action.

By following these points, you can ensure that Docker is installed, Docker Compose is configured, and the environment is set up smoothly within Docker containers.