ARG PYTHON_VERSION=3.12

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    USER=caltrans

# create non-root $USER and home directory
RUN useradd --create-home --shell /bin/bash $USER && \
    # setup directories and permissions
    mkdir -p /$USER/app && \
    chown -R $USER:$USER /$USER

# enter source directory
WORKDIR /$USER

COPY LICENSE app/LICENSE

# switch to non-root $USER
USER $USER

# update env for local pip installs
# see https://docs.python.org/3/using/cmdline.html#envvar-PYTHONUSERBASE
# since all `pip install` commands are in the context of $USER
# $PYTHONUSERBASE is the location used by default
ENV PATH="$PATH:/$USER/.local/bin" \
    PYTHONUSERBASE="/$USER/.local"

WORKDIR /$USER/app

ENV PYTHONPATH="$PYTHONPATH:/$USER/app"

EXPOSE 8501

COPY streamlit_app streamlit_app

RUN pip install -r streamlit_app/requirements.txt

ENTRYPOINT ["./streamlit_app/entrypoint.sh"]
