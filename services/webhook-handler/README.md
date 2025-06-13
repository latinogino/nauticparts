# Unused Services - Architectural Decision

The following services were initially planned but are not implemented due to simplified architecture using existing MCP servers:

## Webhook Handler Service - NOT IMPLEMENTED

**Original Plan**: Custom webhook handler to receive Paperless NGX webhooks and communicate with Claude AI

**Current Solution**: Use existing **nloui/paperless-mcp** server that provides direct Claude Desktop integration with Paperless NGX API

**Benefits of Current Approach**:
- No custom webhook infrastructure needed
- Battle-tested, community-maintained solution
- Direct MCP integration with Claude Desktop
- Full Paperless NGX API coverage

## Image Extraction Service - OPTIONAL/FUTURE

**Status**: Marked as optional for future implementation

**Reason**: Focus on core document management workflow first

**Current Workflow**: 
1. Documents ? Paperless NGX ? Claude analysis via MCP
2. Image extraction can be added later without disrupting core functionality

## Configuration Notes

Instead of custom services, configure Claude Desktop MCP:

```json
{
  "mcpServers": {
    "paperless": {
      "command": "npx",
      "args": ["paperless-mcp", "http://your-oci-server:8000", "your-paperless-api-token"]
    }
  }
}
```

This provides all document management capabilities through Claude Desktop directly.