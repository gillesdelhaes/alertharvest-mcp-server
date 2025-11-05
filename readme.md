# AlertHarvest MCP Server

A Model Context Protocol (MCP) server that provides an interface to the AlertHarvest monitoring alert aggregation and dispatch system.

## Purpose

This MCP server provides a secure interface for AI assistants to interact with AlertHarvest, allowing them to create, acknowledge, and manage monitoring alerts from any source. AlertHarvest acts as a single pane of glass for monitoring alerts with automation capabilities.

## Features

### Current Implementation

- **`create_alert`** - Create a new monitoring alert with location, severity, message, source, and timestamp
- **`acknowledge_alert`** - Acknowledge a specific alert by ID to mark it as seen
- **`acknowledge_alerts_bulk`** - Acknowledge multiple alerts at once using comma-separated IDs
- **`unacknowledge_alert`** - Unacknowledge a specific alert to mark it as unread again
- **`close_alert`** - Close a specific alert by ID to mark it as resolved
- **`close_alerts_bulk`** - Close multiple alerts at once using comma-separated IDs
- **`close_expired_alerts`** - Automatically close all expired alerts based on AlertHarvest's rules

## Prerequisites

- Docker Desktop with MCP Toolkit enabled
- Docker MCP CLI plugin (`docker mcp` command)
- AlertHarvest instance running (default: http://127.0.0.1:8000)

## Installation

See the step-by-step instructions provided with the files.

## Configuration

By default, the server connects to AlertHarvest at `http://127.0.0.1:8000`. To use a different URL:
```bash
docker mcp secret set ALERTHARVEST_URL="http://your-alertharvest-instance:8000"
```

## Usage Examples

In Claude Desktop, you can ask:

### Creating Alerts
- "Create a critical alert for server-01 from Prometheus saying 'High CPU usage detected' at production datacenter"
- "Post an alert with low severity for network-switch-05 from Nagios with message 'Link flapping detected'"
- "Create a monitoring alert: location is 'web-server-03', severity high, message 'Memory usage at 95%', source is 'Zabbix'"

### Acknowledging Alerts
- "Acknowledge alert number 42"
- "Mark alerts 15, 16, and 17 as acknowledged"
- "Acknowledge alerts in bulk: 100, 101, 102, 103"

### Unacknowledging Alerts
- "Unacknowledge alert 42"
- "Mark alert 15 as unread again"

### Closing Alerts
- "Close alert 42"
- "Close alerts 50, 51, 52, 53"
- "Close all expired alerts"

## Architecture
```
Claude Desktop → MCP Gateway → AlertHarvest MCP Server → AlertHarvest API
                                                           ↓
                                              Docker Desktop Secrets
                                                (ALERTHARVEST_URL)
```

## Development

### Local Testing
```bash
# Set environment variables for testing
export ALERTHARVEST_URL="http://127.0.0.1:8000"

# Run directly
python alertharvest_server.py

# Test MCP protocol
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | python alertharvest_server.py
```

### Adding New Tools

1. Add the function to `alertharvest_server.py`
2. Decorate with `@mcp.tool()`
3. Update the catalog entry with the new tool name
4. Rebuild the Docker image

## Alert Severity Levels

Valid severity levels for alerts:
- `CRITICAL` - Highest priority
- `MAJOR` - Medium priority
- `WARNING` - Lower priority

## Troubleshooting

### Tools Not Appearing
- Verify Docker image built successfully: `docker images | grep alertharvest`
- Check catalog and registry files
- Ensure Claude Desktop config includes custom catalog
- Restart Claude Desktop

### Connection Errors
- Verify AlertHarvest is running and accessible
- Check ALERTHARVEST_URL is correctly set
- Test connectivity: `curl http://127.0.0.1:8000`

### API Errors
- Ensure AlertHarvest API is responding
- Check AlertHarvest logs for errors
- Verify alert data format is correct

## Security Considerations

- AlertHarvest URL stored in Docker Desktop secrets
- Never hardcode URLs or credentials
- Running as non-root user
- Sensitive data never logged

## Future Enhancements

Potential features for future versions:
- List/query alerts with filtering
- Update alert severity or message
- Create automation rules
- Configure notification modules
- Bulk operations with more control

## License

MIT License
