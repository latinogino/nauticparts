# Webhook Handler Service

Processes Paperless NGX webhooks and communicates with Claude AI via MCP for document analysis and product recognition.

## Features

- **Webhook Processing**: Receives Paperless NGX document webhooks
- **Claude Integration**: Communicates with Claude Desktop via MCP protocol
- **Product Recognition**: Triggers AI analysis for product identification
- **User Confirmation**: Manages approval workflow for ERP integration
- **Health Monitoring**: Built-in status and health endpoints

## API Endpoints

- `POST /webhook` - Paperless NGX webhook receiver
- `GET /health` - Health check
- `GET /status` - Service status and statistics
- `POST /confirm` - User confirmation endpoint

## Configuration

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `CLAUDE_MCP_URL` | - | Claude MCP connection URL |
| `PAPERLESS_API_URL` | `http://paperless-ngx:8000` | Paperless NGX API URL |
| `PAPERLESS_API_TOKEN` | - | Paperless NGX API token |
| `LOG_LEVEL` | `INFO` | Logging level |

## Workflow

1. Receive webhook from Paperless NGX when document is processed
2. Fetch document content via Paperless API
3. Send to Claude AI for product analysis
4. If product detected, request user confirmation
5. On approval, trigger Dolibarr connector

## Docker

```bash
docker build -t nauticparts-webhook-handler .
docker run -d \
  --name webhook-handler \
  -p 3000:3000 \
  -e PAPERLESS_API_TOKEN=your_token \
  nauticparts-webhook-handler
```