FROM caltrans/pems:web

COPY . .

# install devcontainer requirements
RUN pip install -e .[dev,test]

# install docs requirements
RUN pip install --no-cache-dir -r docs/requirements.txt

# install streamlit requirements
RUN pip install --no-cache-dir -r streamlit_app/requirements.txt

# install AWS CLI and Copilot CLI (requires root permissions)
USER root
# download AWS CLIs to /tmp to avoid write error (23) from curl command
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

RUN curl -Lo copilot https://github.com/aws/copilot-cli/releases/latest/download/copilot-linux \
    && chmod +x copilot \
    && mv copilot /usr/local/bin/copilot

# Switch back to non-root user and app directory
USER $USER
WORKDIR /$USER/app
