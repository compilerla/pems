ARG PYTHON_VERSION=3.12

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    USER=caltrans

# create non-root $USER and home directory
RUN useradd --create-home --shell /bin/bash $USER && \
    chown -R $USER /home/$USER

# switch to $USER
USER $USER

# enter src directory
WORKDIR /home/$USER/src

# update PATH for local pip installs
ENV PATH="$PATH:/home/$USER/.local/bin"

# upgrade pip
RUN python -m pip install --upgrade pip

# copy assets
COPY . .

# install devcontainer requirements
RUN pip install --no-cache-dir -r .devcontainer/requirements.txt

# install docs requirements
RUN pip install --no-cache-dir -r docs/requirements.txt

# install pre-commit environments in throwaway Git repository
# https://stackoverflow.com/a/68758943
RUN git init . && \
    pre-commit install-hooks && \
    rm -rf .git

CMD sleep infinity

ENTRYPOINT []
