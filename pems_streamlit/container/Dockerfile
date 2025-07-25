ARG PYTHON_VERSION=3.12

# multi-stage build
#
# stage 1: builds the package wheel from source
#          using the git metadata for version info
FROM python:${PYTHON_VERSION} AS build_wheel
WORKDIR /build

# install build tools
RUN python -m pip install --upgrade pip wheel setuptools_scm

# copy source files
COPY . .
RUN git config --global --add safe.directory /build

# build wheels for local packages AND downloads
# wheels for all their dependencies from PyPI
# creating a "wheelhouse"
RUN pip wheel --wheel-dir /wheels ./pems_data ./pems_streamlit

# multi-stage build
#
# stage 2: installs the wheel in a fresh base container
#          using the pre-built package, and copying only needed source
FROM python:${PYTHON_VERSION} AS app_container

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    USER=caltrans

EXPOSE 8501

# create non-root $USER and home directory
RUN useradd --create-home --shell /bin/bash $USER && \
    python -m pip install --upgrade pip

COPY LICENSE LICENSE

# switch to non-root $USER
USER $USER

# update env for local pip installs
# see https://docs.python.org/3/using/cmdline.html#envvar-PYTHONUSERBASE
# since all `pip install` commands are in the context of $USER
# $PYTHONUSERBASE is the location used by default
ENV PATH="$PATH:/$USER/.local/bin" \
    PYTHONUSERBASE="/$USER/.local" \
    PYTHONPATH="$PYTHONPATH:/$USER/app"

WORKDIR /$USER/app

COPY .streamlit .streamlit
COPY pems_streamlit/container/entrypoint.sh entrypoint.sh
COPY pems_streamlit/container/run.py run.py

# copy the entire, now-complete wheelhouse from the build stage
COPY --from=build_wheel /wheels /wheels

# install pems_streamlit using only the local wheels directory
RUN pip install --no-index --find-links=/wheels pems_streamlit

ENTRYPOINT ["./entrypoint.sh"]
