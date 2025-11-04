# AlertHarvest MCP Server - Implementation Details

## Overview

This MCP server provides integration with AlertHarvest, a monitoring alert aggregation and dispatch system. It allows AI assistants to create, acknowledge, and manage monitoring alerts through a clean API interface.

## AlertHarvest Background

AlertHarvest is a monitoring software that provides:
- A centralized single pane of glass for monitoring alerts
- Aggregation from any monitoring source
- Dispatch to any target
- Automation capabilities
- Discord module integration (active by default)

## Tool Descriptions

### create_alert
Creates a new monitoring alert in AlertHarvest.

**Parameters:**
- `location` (required): Physical or logical location of the alert (e.g., "server-01", "datacenter-A")
- `severity` (required): Alert severity level (critical, high, medium, low, info)
- `message` (required): Descriptive message about the alert
- `source` (required): Monitoring system that generated the alert (e.g., "Prometheus", "Nagios")
- `timestamp` (optional): ISO format timestamp; auto-generated if not provided

**Use Cases:**
- Forwarding alerts from monitoring systems
- Creating manual alerts for incidents
- Testing alert workflows
- Integration with other automation tools

### acknowledge_alert
Marks a single alert as acknowledged (seen).

**Parameters:**
- `alert_id` (required): Numeric ID of the alert

**Use Cases:**
- Mark alerts as seen without closing them
- Track which alerts have been reviewed
- Workflow management for on-call rotations

### acknowledge_alerts_bulk
Acknowledges multiple alerts at once.

**Parameters:**
- `alert_ids` (required): Comma-separated list of alert IDs

**Use Cases:**
- Batch acknowledge related alerts
- Clear alert backlog efficiently
- Acknowledge alerts after scheduled maintenance

### unacknowledge_alert
Removes acknowledgment from an alert, marking it as unread.

**Parameters:**
- `alert_id` (required): Numeric ID of the alert

**Use Cases:**
- Re-escalate an alert that needs attention
- Undo accidental acknowledgment
- Workflow correction

### close_alert
Closes a single alert, marking it as resolved.

**Parameters:**
- `alert_id` (required): Numeric ID of the alert

**Use Cases:**
- Mark resolved incidents
- Clean up false positives
- Complete alert lifecycle

### close_alerts_bulk
Closes multiple alerts at once.

**Parameters:**
- `alert_ids` (required): Comma-separated list of alert IDs

**Use Cases:**
- Bulk close after incident resolution
- Clean up multiple related alerts
- Post-maintenance cleanup

### close_expired_alerts
Automatically closes all alerts that have exceeded their expiration time.

**Parameters:** None

**Use Cases:**
- Scheduled cleanup of old alerts
- Automatic housekeeping
- Prevent alert accumulation

## Implementation Notes

### Error Handling
All tools include comprehensive error handling for:
- Missing required parameters
- Invalid parameter formats
- HTTP errors from AlertHarvest API
- Network connectivity issues
- Invalid alert IDs

### Input Validation
- Alert IDs must be numeric integers
- Severity levels are validated against allowed values
- All string inputs are trimmed of whitespace
- Empty strings are rejected for required parameters

### Response Formatting
All responses use emoji indicators:
- ✅ for successful operations
- ❌ for errors
- 📍 for location
- ⚠️ for severity
- 💬 for messages
- 🔗 for source
- ⏱️ for timestamp

### Logging
All operations are logged to stderr for debugging:
- Operation type and parameters
- HTTP errors with status codes
- Exception details

## Configuration

### Environment Variables
- `ALERTHARVEST_URL`: Base URL of AlertHarvest instance (default: http://127.0.0.1:8000)

### API Endpoints Used
- POST `/api/create_alert/` - Create new alert
- PUT `/api/acknowledge_alert/{id}` - Acknowledge single alert
- PUT `/api/acknowledge_alerts_bulk/` - Acknowledge multiple alerts
- PUT `/api/unacknowledge_alert/{id}` - Unacknowledge alert
- PUT `/api/close_alert/{id}` - Close single alert
- PUT `/api/close_alerts_bulk/` - Close multiple alerts
- PUT `/api/close_expired_alerts/` - Close expired alerts

## Integration Patterns

### With Monitoring Systems
```python
# Example: Forward Prometheus alert
create_alert(
    location="web-server-01",
    severity="critical",
    message="HTTP endpoint down: /api/health",
    source="Prometheus",
    timestamp="2025-01-15T10:30:00Z"
)
```

### Bulk Operations
```python
# Acknowledge multiple related alerts
acknowledge_alerts_bulk(alert_ids="42,43,44,45")

# Close resolved incident alerts
close_alerts_bulk(alert_ids="100,101,102")
```

### Automated Cleanup
```python
# Schedule periodic cleanup
close_expired_alerts()
```

## Testing

### Manual Testing
```bash
# Test alert creation
curl -X POST http://127.0.0.1:8000/api/create_alert/ \
  -H "Content-Type: application/json" \
  -d '{
    "location": "test-server",
    "severity": "info",
    "message": "Test alert",
    "source": "manual",
    "timestamp": "2025-01-15T12:00:00Z"
  }'

# Test alert acknowledgment
curl -X PUT http://127.0.0.1:8000/api/acknowledge_alert/1
```

## Limitations

### Current Version
- No authentication required (AlertHarvest API is currently open)
- Cannot query/list existing alerts
- Cannot modify alert properties after creation
- Cannot create automation rules via API

### Future API Additions
The AlertHarvest project is actively developed. Future versions may include:
- Alert querying and filtering
- Rule creation and management
- Module configuration
- User authentication
- Webhook integrations

## Best Practices

### Alert Creation
- Use consistent location naming conventions
- Choose appropriate severity levels
- Include actionable information in messages
- Always specify the source system
- Let timestamps auto-generate unless backdating

### Alert Management
- Acknowledge alerts before investigating
- Close alerts only when fully resolved
- Use bulk operations for efficiency
- Run expired alert cleanup regularly

### Integration
- Validate data before creating alerts
- Handle API errors gracefully
- Log all operations for audit trails
- Use meaningful source identifiers

## Support

For AlertHarvest support and contributions:
- Discord: https://discord.gg/hduVhv7VaA
- GitHub: https://github.com/gillesdelhaes/AlertHarvest

## License

MIT License
