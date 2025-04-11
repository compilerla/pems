FROM caltrans/pems:app

COPY . .

# install devcontainer requirements
RUN pip install -e .[dev,test]

# install docs requirements
RUN pip install --no-cache-dir -r docs/requirements.txt

# install streamlit requirements
RUN pip install --no-cache-dir -r streamlit_app/requirements.txt
