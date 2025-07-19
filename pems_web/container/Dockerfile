ARG PYTHON_VERSION=3.12

# multi-stage build
#
# stage 1: builds the package wheel from source
#          using the git metadata for version info
FROM python:${PYTHON_VERSION} AS build_wheel
WORKDIR /build

# upgrade pip, install build dependencies
RUN python -m pip install --upgrade pip build setuptools_scm

# copy source files
COPY . .
RUN git config --global --add safe.directory /build

# Move into directory to run the build
WORKDIR /build/pems_web

# build package
RUN python -m build

# multi-stage build
#
# stage 2: installs the wheel in a fresh base container
#          using the pre-built package, and copying only needed source
FROM python:${PYTHON_VERSION} AS app_container

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    USER=caltrans
ENV RUNTIME_DIR="/${USER}/app"
ENV STATIC_DIR="${RUNTIME_DIR}/pems_web/src/pems_web/static"

EXPOSE 8000

    # create non-root $USER and home directory
RUN useradd --create-home --shell /bin/bash $USER && \
    # setup $USER permissions for nginx
    mkdir -p /var/cache/nginx && \
    chown -R $USER:$USER /var/cache/nginx && \
    mkdir -p /var/lib/nginx && \
    chown -R $USER:$USER /var/lib/nginx && \
    mkdir -p /var/log/nginx && \
    chown -R $USER:$USER /var/log/nginx && \
    touch /var/log/nginx/error.log && \
    chown $USER:$USER /var/log/nginx/error.log && \
    touch /var/run/nginx.pid && \
    chown -R $USER:$USER /var/run/nginx.pid && \
    # setup directories and permissions for gunicorn, (eventual) app
    mkdir -p /$USER/app && \
    mkdir -p /$USER/run && \
    # install server components
    apt-get update && \
    apt-get install -qq --no-install-recommends build-essential nginx gettext && \
    python -m pip install --upgrade pip pipdeptree

# install AWS CLI (requires root permissions)
# download AWS CLI to /tmp to avoid write error (23) from curl command
WORKDIR /tmp
RUN HOST_ARCH=$(uname -m) && \
    case "$HOST_ARCH" in \
      x86_64) HOST_ARCH="amd64" ;; \
      aarch64) HOST_ARCH="arm64" ;; \
    esac \
    && if [ "$HOST_ARCH" = "amd64" ]; then \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"; \
    elif [ "$HOST_ARCH" = "arm64" ]; then \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip"; \
    fi \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -rf aws awscliv2.zip

# enter source directory
WORKDIR /$USER

# copy runtime files
COPY LICENSE LICENSE
COPY pems_web/container/gunicorn.conf.py run/gunicorn.conf.py
COPY pems_web/container/nginx.conf /etc/nginx/nginx.conf

WORKDIR $RUNTIME_DIR

COPY pems_web/container/certs/aws_global_postgres_ca_bundle.pem certs/aws_global_postgres_ca_bundle.pem
COPY manage.py manage.py
COPY bin bin
COPY pems_web/src/pems_web/local_fixtures.json pems_web/src/pems_web/local_fixtures.json
COPY pems_web/src/pems_web/static $STATIC_DIR
COPY --from=build_wheel /build/pems_web/dist /wheels

RUN chown -R $USER:$USER /$USER

# switch to non-root $USER
USER $USER

# update env for local pip installs
# see https://docs.python.org/3/using/cmdline.html#envvar-PYTHONUSERBASE
# since all `pip install` commands are in the context of $USER
# $PYTHONUSERBASE is the location used by default
ENV PATH="$PATH:/$USER/.local/bin" \
    PYTHONUSERBASE="/$USER/.local" \
    GUNICORN_CONF="/$USER/run/gunicorn.conf.py"

# install package wheel
RUN pip install $(find /wheels -name pems_web*.whl) \
# write static requirements file
    && pipdeptree >> $STATIC_DIR/requirements.txt

# configure container executable
ENTRYPOINT ["/bin/bash"]
CMD ["bin/start.sh"]
