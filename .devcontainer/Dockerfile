FROM caltrans/pems:app

COPY . .
# install devcontainer requirements
RUN pip install -e .[dev]

# install docs requirements
RUN pip install --no-cache-dir -r docs/requirements.txt
