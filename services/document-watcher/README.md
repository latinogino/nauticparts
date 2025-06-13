# Document Watcher Service

Monitors the Nextcloud shared folder for new PDF/DOCX documents and automatically imports them to Paperless NGX consume folder.

## Features

- **Real-time monitoring** of file system changes using watchdog
- **Automatic import** to Paperless NGX consume folder
- **Metadata generation** with auto-tagging for imported documents
- **Duplicate handling** with filename conflict resolution
- **Health check endpoint** for monitoring
- **Force processing** endpoint for manual file processing
- **Comprehensive logging** with rotation

## Simplified Workflow

1. **Monitor** Nextcloud shared folder for new documents
2. **Validate** file types (PDF, DOCX, DOC)
3. **Copy** files to Paperless NGX consume folder
4. **Generate** metadata JSON files for enhanced import
5. **Log** all operations for monitoring

## Configuration

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `WATCH_FOLDER` | `/shared` | Folder to monitor for new documents |
| `PAPERLESS_CONSUME_FOLDER` | `/paperless-consume` | Paperless NGX consume directory |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |

## Supported File Types

- PDF (.pdf)
- Microsoft Word (.docx, .doc)

## API Endpoints

- `GET /health` - Health check
- `GET /status` - Service status and statistics
- `POST /force-process/{filename}` - Force process a specific file

## Generated Metadata

Each imported document gets an optional metadata JSON file:

```json
{
  "title": "document-name",
  "created": "2024-01-19",
  "source": "Nextcloud Auto-Import",
  "tags": ["auto-imported", "nautical-parts"]
}
```

## Docker Usage

```bash
# Build and run
docker build -t nauticparts-document-watcher .
docker run -d \
  --name document-watcher \
  -v /path/to/shared:/shared \
  -v /path/to/paperless/consume:/paperless-consume \
  -e WATCH_FOLDER=/shared \
  nauticparts-document-watcher
```

## Integration with Paperless NGX

Once files are copied to the consume folder, Paperless NGX will:

1. **OCR Processing** - Extract text from documents
2. **Auto-Tagging** - Apply rules-based tags
3. **Indexing** - Make content searchable
4. **Webhook Triggers** - Optional webhook notifications

## Claude Integration

After Paperless NGX processes documents, use Claude Desktop with Paperless MCP:

```bash
# Install Paperless MCP
npm install -g paperless-mcp
```

Then query via Claude:
- *"Show me the latest imported documents"*
- *"Search for nautical parts documentation"*
- *"Analyze the newest product specification"*

## Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
WATCH_FOLDER=./test_data python watcher.py
```

## Monitoring

Check service health:
```bash
curl http://localhost:8080/health
curl http://localhost:8080/status
```

Force process a file:
```bash
curl -X POST http://localhost:8080/force-process/document.pdf
```