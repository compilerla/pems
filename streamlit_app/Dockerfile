FROM caltrans/pems:app

EXPOSE 8501

COPY streamlit_app streamlit_app

RUN pip install -r streamlit_app/requirements.txt

ENTRYPOINT ["streamlit", "run", "streamlit_app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
