FROM python:3.13-slim
ARG TAILSCALE_VERSION=1.104.5
ARG TAILSCALE_SHA256=e900b0e6e25023a1e504b2c237ce2a32ea0535e006f8c1a1097a490886493b6c
ENV PYTHONUNBUFFERED=1
ADD https://pkgs.tailscale.com/stable/tailscale_${TAILSCALE_VERSION}_arm64.tgz /tmp/tailscale.tgz
RUN echo "${TAILSCALE_SHA256}  /tmp/tailscale.tgz" | sha256sum -c - \
 && tar -xzf /tmp/tailscale.tgz -C /tmp \
 && install -m 0755 /tmp/tailscale_${TAILSCALE_VERSION}_arm64/tailscale /tmp/tailscale_${TAILSCALE_VERSION}_arm64/tailscaled /usr/local/bin/ \
 && rm -rf /tmp/tailscale*
WORKDIR /app
COPY requirements-server.txt ./
RUN pip install --no-cache-dir -r requirements-server.txt
COPY server.py BUILD ./
COPY engine ./engine
COPY web ./web
COPY tracks ./tracks
COPY data/vocabulary.csv ./data/vocabulary.csv
COPY start.py options.py run.sh /
RUN chmod a+x /run.sh
CMD ["/run.sh"]
