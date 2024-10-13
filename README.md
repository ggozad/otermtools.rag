# oterm.tools.rag

`oterm.tools.rag` is an [Ollama](https://github.com/ollama/ollama) tool for adding RAG (Retrieval-Augmented Generation) capabilities to the terminal-based chat client [oterm](https://github.com/ggozad/oterm).

THIS IS A WORK IN PROGRESS.

## Installation

Start by building and running the the docker containers necessary.
First, set a password for the postgres database in `secrets/psql.env`:
```bash
POSTGRES_PASSWORD = psql
```

Then, run the docker compose file in the root of the repository:

```bash
docker-compose up -d 
```


