FROM python:3.13-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements-server.txt ./
RUN pip install --no-cache-dir -r requirements-server.txt
COPY server.py ./
COPY engine ./engine
COPY web ./web
COPY tracks ./tracks
COPY data/vocabulary.csv ./data/vocabulary.csv
COPY start.py run.sh /
RUN chmod a+x /run.sh
CMD ["/run.sh"]
