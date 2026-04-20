FROM python:3.9.21-slim-bullseye

ENV DEBIAN_FRONTEND=noninteractive

# ---------------------------
# System dependencies
# ---------------------------
RUN apt-get update && apt-get --yes upgrade && \
    apt-get install --yes --no-install-recommends \
      net-tools \
      procps \
      tini \
      libmagic1 \
      libpq-dev \
      libxml2-dev \
      libxslt-dev \
      libgeos-dev \
      libssl-dev \
      libffi-dev \
      postgresql-client \
      build-essential \
      git-core \
      wget \
      curl \
      proj-bin \
      libxslt1-dev \
      libgeos-c1v5 \
      libgdal-dev \
      zlib1g-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ---------------------------
# Python tooling (CRITICAL FIX)
# ---------------------------
RUN python -m pip install --upgrade pip setuptools==58.1.0 wheel

# ---------------------------
# Create non-root user
# ---------------------------
RUN useradd --create-home appuser && \
    mkdir -p /usr/local/src && \
    chown -R appuser:appuser /usr/local/src

# ---------------------------
# Install Poetry as root (allows site-wide installs in /usr/local/lib)
# ---------------------------
ENV POETRY_VIRTUALENVS_OPTIONS_SYSTEM_SITE_PACKAGES=true

RUN python -m pip install --no-cache-dir "poetry==1.4.2"

# Ensure user site has setuptools/pkg_resources for build isolation fallbacks
RUN python -m pip install --upgrade setuptools==58.1.0

# ---------------------------
# App directories
# ---------------------------
RUN mkdir -p /home/appuser/app /home/appuser/data && \
    chown -R appuser:appuser /home/appuser

# ---------------------------
# Environment variables
# ---------------------------
ENV PYTHONFAULTHANDLER=1 \
    PIP_CONSTRAINT=/home/appuser/pip-constraints.txt \
    PIP_BUILD_CONSTRAINT=/home/appuser/pip-constraints.txt \
    PIP_NO_BUILD_ISOLATION=1 \
    POETRY_INSTALLER_NO_BUILD_ISOLATION=1 \
    POETRY_INSTALLER_MODERN_INSTALLATION=false \
    POETRY_EXPERIMENTAL_NEW_INSTALLER=false \
    POETRY_VIRTUALENVS_CREATE=false \
    CKAN_INI=/home/appuser/ckan.ini

WORKDIR /home/appuser/app

# ---------------------------
# Copy dependency file first (better caching)
# ---------------------------
COPY --chown=appuser:appuser pyproject.toml ./

# ---------------------------
# Constraints (fixes pkg_resources issues in builds)
# ---------------------------
RUN printf "setuptools==58.1.0\nCython<3\n" > /home/appuser/pip-constraints.txt && \
    mkdir -p /home/appuser/.config/pip && \
    printf "[install]\nconstraint = /home/appuser/pip-constraints.txt\n" > /home/appuser/.config/pip/pip.conf

# flask-multistatic's legacy setup.py imports pkg_resources and can fail under PEP517 isolation
RUN PIP_USE_PEP517=0 python -m pip install --no-cache-dir "flask-multistatic==1.0"

# ---------------------------
# Expose service port
# ---------------------------
EXPOSE 5000

# ---------------------------
# Copy full application
# ---------------------------
COPY --chown=appuser:appuser . .

RUN poetry lock --no-update && \
    poetry install --only main

# CKAN builds JS translation files under this directory at runtime.
RUN mkdir -p /usr/local/lib/python3.9/site-packages/ckan/public/base/i18n && \
    chown -R appuser:appuser /usr/local/lib/python3.9/site-packages/ckan/public/base/i18n

# ---------------------------
# Git commit tracking
# ---------------------------
ARG GIT_COMMIT
ENV GIT_COMMIT=$GIT_COMMIT

RUN echo $GIT_COMMIT > /home/appuser/git-commit.txt

# ---------------------------
# Bytecode compile (faster startup)
# ---------------------------
RUN poetry run python -c "import compileall; compileall.compile_path(maxlevels=10)"

# Drop privileges for runtime
USER appuser

# ---------------------------
# Entrypoint
# ---------------------------
ENTRYPOINT ["tini", "-g", "--", "poetry", "run", "docker_entrypoint"]
CMD ["launch-gunicorn"]