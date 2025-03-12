FROM python:3.10-slim-bullseye

ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL=C.UTF-8 LANG=C.UTF-8

RUN \
    apt-get update && \
    apt-get install --no-install-recommends -y \ 
    curl ca-certificates \ 
    build-essential libpq-dev \
    gettext poppler-utils && \
    rm -r /var/cache/apt /var/lib/apt


# Setup uv
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

RUN mkdir /documents
ADD . /app


WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync
# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"
CMD ["fastapi", "dev", "src/haiku/rag/app.py", "--host", "0.0.0.0"]