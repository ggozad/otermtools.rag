FROM python:3.10-slim-bullseye

ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL=C.UTF-8 LANG=C.UTF-8

RUN \
    apt-get update && \
    apt-get install --no-install-recommends -y \ 
    curl ca-certificates \ 
    build-essential libpq-dev \
    gettext poppler-utils vim && \
    rm -r /var/cache/apt /var/lib/apt


# Setup uv
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.cargo/bin/:$PATH"

ADD . /app

WORKDIR /app
RUN uv sync

# Use the virtual environment automatically
ENV VIRTUAL_ENV=/app/.venv
# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"
CMD ["fastapi", "dev", "src/oterm/tools/rag/app.py", "--host", "0.0.0.0"]