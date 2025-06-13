# Image Extractor Service - OPTIONAL/FUTURE

This service is marked as **optional** for future implementation to focus on core functionality first.

## Planned Features (Future Implementation)

- **PDF Processing**: PyMuPDF-based image extraction with page information
- **DOCX Processing**: Direct image extraction from Office documents  
- **Metadata Preservation**: Structured JSON metadata for each extracted image
- **REST API**: Simple HTTP interface for extraction requests
- **Integration**: Automatic image processing before Paperless NGX import

## Current Status: NOT IMPLEMENTED

**Reason**: Simplified architecture focusing on document management workflow

**Current Priority**: 
1. ? Document monitoring and import
2. ? Paperless NGX integration via MCP
3. ? Claude AI analysis capabilities
4. ? Dolibarr ERP integration
5. ? Image extraction (future enhancement)

## Future Integration Plan

When implemented, this service would:

1. **Pre-process documents** before Paperless NGX import
2. **Extract embedded images** from PDF/DOCX files
3. **Generate metadata** linking images to source documents
4. **Store images** in organized folder structure
5. **Enable image-based queries** via Claude AI

## Alternative Approach

For immediate image needs, use Paperless NGX built-in capabilities:
- Paperless NGX already extracts and indexes document images
- Claude Desktop can analyze documents including embedded images
- Manual image extraction can be done as needed

## Development Notes

If implementing this service later:

```bash
# Planned dependencies
pip install PyMuPDF python-docx Pillow fastapi uvicorn

# Planned API endpoints
POST /extract - Extract images from document
GET /health - Health check
GET /status - Service status
```

## Focus on Core Value

Current implementation prioritizes:
- **Document workflow automation** ?
- **AI-powered analysis** ?  
- **ERP integration** ?
- **User experience** ?

Image extraction adds value but is not essential for the core workflow.