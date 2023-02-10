############################################################
# Dockerfile to build Python / Django / MySQL small container images
# Based on python slim debian buster
############################################################

# Use an official Python runtime as a parent image

FROM python:3.10.8-slim-buster as common-base

LABEL MANTAINER="Suryo Prasetyo W <the.oyrus@gmail.com>"
# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONIOENCODING utf-8
ENV DJANGO_SETTINGS_MODULE core.settings
ENV APP_PATH app
ENV APP_USER aplikasi

#############################
# Stage 1: Build
#############################
FROM common-base as builder

# Set the working directory to /app
RUN mkdir /${APP_PATH}
WORKDIR /$APP_PATH

# Install system package for building
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc default-libmysqlclient-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/

RUN python -m venv /${APP_PATH}/.venv
ENV PATH="/$APP_PATH/.venv/bin:$PATH"
ENV VIRTUAL_ENV=/${APP_PATH}/.venv/

# Install python package
COPY requirements.txt .
RUN pip install --no-cache-dir --no-compile -r requirements.txt

#############################
# Stage 2: Run application
#############################
FROM common-base as run

# Set the working directory to /app
RUN mkdir -p /${APP_PATH}
WORKDIR /$APP_PATH

# Install system package for running
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/

## always good to run our source code with a different user other than root user
RUN addgroup --system ${APP_USER} --gid 1000 && adduser --system --no-create-home --group ${APP_USER} --uid 1000
RUN chown -R ${APP_USER}:${APP_USER} /${APP_PATH} && chmod -R 755 /${APP_PATH}

# copy app source
COPY --chown=${APP_USER}:${APP_USER} . .
COPY --chown=${APP_USER}:${APP_USER} --from=builder /${APP_PATH}/.venv/ /${APP_PATH}/.venv/

# activate virtual enviroment
ENV VIRTUAL_ENV=/${APP_PATH}/.venv/
ENV PATH="/$APP_PATH/.venv/bin:$PATH"

# switch to our user
USER ${APP_USER}

RUN chmod +x docker-entrypoint.sh
EXPOSE 8000
CMD ["/app/docker-entrypoint.sh"]
