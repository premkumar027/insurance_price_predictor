# install python 3.10
FROM python:3.12-slim

# set work directory
WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY app/ ./

# expose port
EXPOSE 8000 8501

# run server
CMD bash -c 'uvicorn app:app --host 0.0.0.0 --port 8000 & streamlit run frontend.py --server.address 0.0.0.0 --server.port 8501'
