# Dolibarr Connector Service

Integrates with Dolibarr ERP system to automatically create products based on Claude AI analysis results.

## Features

- **REST API Integration**: Connects to Dolibarr REST API
- **Product Creation**: Automatic product record creation
- **Metadata Mapping**: Maps document metadata to ERP fields
- **Error Handling**: Robust error handling and retry logic
- **Validation**: Data validation before ERP submission

## API Endpoints

- `POST /create-product` - Create product in Dolibarr
- `GET /health` - Health check
- `GET /status` - Service status
- `GET /products` - List recent products

## Configuration

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `DOLIBARR_URL` | `http://dolibarr:80` | Dolibarr instance URL |
| `DOLIBARR_API_KEY` | - | Dolibarr API key |
| `LOG_LEVEL` | `INFO` | Logging level |

## Product Data Mapping

Claude AI extracted data is mapped to Dolibarr fields:

- `product_name` ? `label`
- `product_number` ? `ref`
- `description` ? `description`
- `category` ? `fk_product_type`
- `price` ? `price` (if available)

## Usage

```bash
# Create product
curl -X POST http://dolibarr-connector:8080/create-product \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Marine Bearing 12345",
    "product_number": "MB-12345",
    "description": "High-quality marine bearing for nautical applications",
    "category": "bearings"
  }'
```

## Docker

```bash
docker build -t nauticparts-dolibarr-connector .
docker run -d \
  --name dolibarr-connector \
  -e DOLIBARR_API_KEY=your_api_key \
  nauticparts-dolibarr-connector
```