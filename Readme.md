# Mini-RAG API

A simple RAG (Retrieval-Augmented Generation) backend built with FastAPI and MongoDB. It allows you to upload files, split them into chunks, and store them for later retrieval.

---

## Stack

- **FastAPI** — REST API
- **MongoDB** (via Motor) — async database
- **LangChain** — document loading and text splitting
- **Docker** — MongoDB container

---

## Project Structure

```
src/
├── main.py                  # App entry point
├── routes/
│   ├── base.py              # Health check route
│   ├── data.py              # Upload & process routes
│   └── schemes/
│       └── data.py          # Request schemas
├── controllers/
│   ├── BaseController.py    # Shared logic
│   ├── DataController.py    # File validation & path generation
│   ├── ProjectController.py # Project directory management
│   └── ProcessController.py # File loading & chunking
├── models/
│   ├── ProjectModel.py      # Project DB operations
│   ├── ChunkModel.py        # Chunk DB operations
│   ├── AssetModel.py        # Asset DB operations
│   └── db_schemes/          # Pydantic schemas (Project, DataChunk, Asset)
├── helpers/
│   └── config.py            # Settings via pydantic-settings
└── assets/files/            # Uploaded files (gitignored)
docker/
└── docker-compose.yml       # MongoDB container
```

---

## Data Model

```
Project (1)
  └── Asset (N)       ← one record per uploaded file
        └── DataChunk (N)  ← text chunks extracted from the file
```

- **Project** : logical workspace identified by a `project_id`
- **Asset** : metadata of an uploaded file (name, size, type, date)
- **DataChunk** : a piece of text extracted and split from a file

> The file itself is stored on disk (`assets/files/{project_id}/`). Only metadata and chunks go into MongoDB.

---

## Setup

### 1. Start MongoDB

```bash
cd docker
docker-compose up -d
```

### 2. Create the `.env` file

```bash
# src/.env
APP_NAME=mini-rag
APP_VERSION=1.0.0
OPENROUTER_API_KEY=your_key_here

FILE_ALLOWED_TYPES=["application/pdf", "text/plain"]
FILE_MAX_SIZE=10
FILE_DEFAULT_CHUNK_SIZE=1048576

MONGODB_URL=mongodb://localhost:27007
MONGODB_DATABASE=mini_rag_db
```

### 3. Install dependencies

```bash
cd src
pip install -r requirements.txt
```

### 4. Run the server

```bash
cd src
uvicorn main:app --reload
```

API available at: `http://localhost:8000`  
Swagger docs: `http://localhost:8000/docs`

---

## API Endpoints

### `GET /api/v1/`
Health check — returns app name and version.

---

### `POST /api/v1/data/upload/{project_id}`
Upload a file to a project.

- **Path param**: `project_id` — alphanumeric project identifier
- **Form data**: `file` — `.txt` or `.pdf`
- **Returns**: `file_id` (MongoDB Asset ID)

```bash
curl -X POST "http://localhost:8000/api/v1/data/upload/myproject" \
  -F "file=@document.pdf"
```

---

### `POST /api/v1/data/process/{project_id}`
Process a file: split it into chunks and store them in MongoDB.

- **Path param**: `project_id`
- **Body (JSON)**:

```json
{
  "file_id": "filename_generated_on_upload.pdf",
  "chunk_size": 200,
  "overlap_size": 40,
  "do_reset": 0
}
```

- `do_reset: 1` → deletes existing chunks for this project before inserting new ones

---

## Supported File Types

| Type | Extension |
|------|-----------|
| Plain text | `.txt` |
| PDF | `.pdf` |

---

## Notes

- Files are stored on disk, not in MongoDB
- `project_id` must be alphanumeric
- Chunk overlap only applies when a chunk exceeds `chunk_size`