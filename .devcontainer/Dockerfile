ARG PYTHON_VERSION=3.12

FROM python:${PYTHON_VERSION}

WORKDIR /tmp

# install AWS CLI and Copilot CLI (requires root permissions)
# download AWS Copilot CLI to /tmp to avoid write error (23) from curl command
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
    && rm -rf aws awscliv2.zip \
    && curl -Lo copilot https://github.com/aws/copilot-cli/releases/latest/download/copilot-linux \
    && chmod +x copilot \
    && mv copilot /usr/local/bin/copilot

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    USER=caltrans
ENV RUNTIME_DIR=/$USER/app

# create non-root $USER and home directory
RUN useradd --create-home --shell /bin/bash $USER \
    && apt-get update \
    && apt-get install -qq --no-install-recommends build-essential gettext \
    && python -m pip install --upgrade pip \
    && mkdir -p "$RUNTIME_DIR"

WORKDIR /$USER/app

# copy source files and update permissions
COPY . .

RUN git config --global --add safe.directory . \
    && chown -R $USER:$USER /$USER

# Switch to non-root user
USER $USER

ENV PATH="$PATH:/$USER/.local/bin" \
    PYTHONUSERBASE="/$USER/.local"

# install devcontainer requirements
RUN pip install -e .[dev,test]

# install docs requirements
RUN pip install --no-cache-dir -r docs/requirements.txt

# install streamlit requirements
RUN pip install --no-cache-dir -r streamlit_app/requirements.txt
