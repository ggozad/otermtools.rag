# otermtools.rag

`otermtools.rag` is an [Ollama](https://github.com/ollama/ollama) tool for adding RAG (Retrieval-Augmented Generation) capabilities to the terminal-based Ollama client [oterm](https://github.com/ggozad/oterm).

**THIS IS A WORK IN PROGRESS.**

## Installation

### Using Docker
Start by building and running the the docker containers necessary:
Clone the repository and navigate to the root of the repository:
```bash
git clone https://github.com/ggozad/otermtools.rag.git
cd otermtools.rag
```

Set a password for the postgres database in `secrets/psql.env`:
```bash
POSTGRES_PASSWORD = psql
```

Then, run the docker compose file in the root of the repository:

```bash
docker-compose up -d 
```

This will start postgres with the `pgvector` extension as well as the store API.
In addition it will monitor any files you have in the mounted `/volumes/documents` directory and index them in the database.

## Using the store API

A bare-bones API is provided to interact with the document store at http://localhost:8000/docs#/

