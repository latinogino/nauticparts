# Image Extractor Service

Extracts images from PDF and DOCX documents with metadata preservation for Paperless NGX integration.

## Features

- **PDF Processing**: PyMuPDF-based image extraction with page information
- **DOCX Processing**: Direct image extraction from Office documents
- **Metadata Preservation**: Structured JSON metadata for each extracted image
- **REST API**: Simple HTTP interface for extraction requests
- **Health Monitoring**: Built-in health check endpoints

## API Endpoints

- `POST /extract` - Extract images from document
- `GET /health` - Health check
- `GET /status` - Service status

## Configuration

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `INPUT_FOLDER` | `/shared` | Folder to monitor for documents |
| `OUTPUT_FOLDER` | `/paperless-media/extracted_images` | Output directory for images |
| `LOG_LEVEL` | `INFO` | Logging level |

## Usage

```bash
# Extract images from a document
curl -X POST http://image-extractor:8080/extract \
  -H "Content-Type: application/json" \
  -d '{"file_path": "/shared/document.pdf"}'
```

## Docker

```bash
docker build -t nauticparts-image-extractor .
docker run -d \
  --name image-extractor \
  -v /path/to/shared:/shared \
  -v /path/to/paperless/media:/paperless-media \
  nauticparts-image-extractor
```