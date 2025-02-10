#! /usr/bin/env python3
"""Manage docker-compose"""

import argparse
import datetime
import logging
import os
import shlex
import sys
import typing
from subprocess import check_output, CalledProcessError

logger = logging.getLogger(__name__)

_FALLBACK_GIT_BRANCH = "main"
_IMAGE_NAME = "saeoss"


def _get_docker_compose_command() -> str:
    """Check if `docker compose` is available, otherwise fallback to `docker-compose`."""
    try:
        check_output(shlex.split("docker compose version"), text=True)
        return "docker compose"
    except (FileNotFoundError, CalledProcessError):
        return "docker-compose"


DOCKER_COMPOSE_CMD = _get_docker_compose_command()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--image-tag")
    parser.add_argument(
        "--compose-file", action="append", default=["docker-compose.yml"]
    )
    subparsers = parser.add_subparsers()
    compose_restart_parser = subparsers.add_parser("db-backup")
    compose_restart_parser.set_defaults(func=run_db_backup)
    compose_up_parser = subparsers.add_parser("up")
    compose_up_parser.set_defaults(func=run_compose_up)
    compose_down_parser = subparsers.add_parser("down")
    compose_down_parser.set_defaults(func=run_compose_down)
    compose_restart_parser = subparsers.add_parser("restart")
    compose_restart_parser.set_defaults(func=run_compose_restart)
    compose_restart_parser.add_argument("service", nargs="+")
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    args.func(args)


def run_compose_up(args):
    image_tag = args.image_tag if args.image_tag else _get_image_tag_name()
    if image_tag is not None:
        exec_env = _set_exec_environment(image_tag)
        logger.info(f"Using {image_tag!r} as the tag for the CKAN image...")
        _run_docker_compose("up --detach", args.compose_file, exec_env)
    else:
        raise SystemExit(
            f"There is no docker image for the current git branch yet, and neither "
            f"for the {_FALLBACK_GIT_BRANCH!r} branch - Please build the image "
            f"first. Aborting..."
        )


def run_compose_down(args):
    image_tag = args.image_tag if args.image_tag else _get_image_tag_name()
    exec_env = (
        _set_exec_environment(image_tag) if image_tag else os.environ.copy()
    )
    _run_docker_compose("down", args.compose_file, exec_env)


def run_compose_restart(args):
    _run_docker_compose(f"restart {' '.join(args.service)}", args.compose_file)


def run_db_backup(args):
    timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    env = os.environ.copy()
    command = _get_compose_command(
        f'exec ckan-db su - postgres -c "pg_dumpall" | gzip -9 > ckan-{timestamp}.sql.gz',
        args.compose_file,
    )
    logger.debug(f"Running: {command!r} with environment {env}")
    sys.stdout.flush()
    sys.stderr.flush()
    os.system(
        f'{DOCKER_COMPOSE_CMD} --project-name=saeoss exec ckan-db su - postgres -c "pg_dumpall" | '
        f"gzip -9 > ckan-{timestamp}.sql.gz"
    )
    os.system(
        f'{DOCKER_COMPOSE_CMD} --project-name=saeoss exec ckan-db su - postgres -c "pg_dumpall" | '
        f"gzip -9 > datastore-{timestamp}.sql.gz"
    )


def _get_compose_command(fragment: str, compose_file: typing.List[str]) -> str:
    files_fragment = " ".join(f"--file={path}" for path in compose_file)
    template = (
        f"{DOCKER_COMPOSE_CMD} --project-name={{project}} {files_fragment} {fragment}"
    )
    return template.format(project="saeoss")


def _get_image_tag_name() -> typing.Optional[str]:
    try:
        current_git_branch = (
            check_output(shlex.split("git rev-parse --abbrev-ref HEAD"), text=True)
            .strip("\n")
            .replace("/", "-")
        )
        existing_image_tags = check_output(
            shlex.split(f"docker images {_IMAGE_NAME} --format '{{{{.Tag}}}}'"),
            text=True,
        ).split("\n")
        if current_git_branch in existing_image_tags:
            logger.info("The current branch already has a built tag, using that...")
            return current_git_branch
        elif _FALLBACK_GIT_BRANCH in existing_image_tags:
            logger.info(
                f"The current branch does not have a built tag,"
                f" using {_FALLBACK_GIT_BRANCH!r} image tag."
            )
            return _FALLBACK_GIT_BRANCH
    except CalledProcessError:
        logger.error("Failed to retrieve git branch or docker images.")
    return None


def _set_exec_environment(image_tag: str) -> typing.Dict[str, str]:
    env = os.environ.copy()
    env["CKAN_IMAGE_TAG"] = image_tag
    env["GIT_BRANCH_NAME"] = image_tag
    return env


def _run_docker_compose(
    command_fragment: str,
    compose_file: typing.List[str],
    environment: typing.Optional[typing.Dict[str, str]] = None,
):
    env = environment or os.environ.copy()
    command = _get_compose_command(command_fragment, compose_file)
    logger.debug(f"Executing command: {command!r} with environment {env}")
    sys.stdout.flush()
    sys.stderr.flush()
    os.execvpe(DOCKER_COMPOSE_CMD.split()[0], shlex.split(command), env)


if __name__ == "__main__":
    main()
