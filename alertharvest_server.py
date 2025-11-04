#!/usr/bin/env python3
"""
Simple AlertHarvest MCP Server - Interface for AlertHarvest monitoring alert API
"""
import os
import sys
import logging
from datetime import datetime, timezone
import httpx
from mcp.server.fastmcp import FastMCP

# Configure logging to stderr
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("alertharvest-server")

# Initialize MCP server
mcp = FastMCP("alertharvest")

# Configuration
ALERTHARVEST_URL = os.environ.get("ALERTHARVEST_URL", "http://127.0.0.1:8000")

# === UTILITY FUNCTIONS ===

def format_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat()

def validate_severity(severity: str) -> bool:
    """Validate severity level."""
    valid_levels = ["CRITICAL", "MAJOR", "WARNING"]
    return severity in valid_levels

# === MCP TOOLS ===

@mcp.tool()
async def create_alert(location: str = "", severity: str = "", message: str = "", source: str = "", timestamp: str = "") -> str:
    """Create a new alert in AlertHarvest with location, severity, message, source, and timestamp."""
    logger.info(f"Creating alert: location={location}, severity={severity}, source={source}")
    
    # Validation
    if not location.strip():
        return "❌ Error: Location is required"
    if not severity.strip():
        return "❌ Error: Severity is required"
    if not message.strip():
        return "❌ Error: Message is required"
    if not source.strip():
        return "❌ Error: Source is required"
    
    # Validate severity level
    if not validate_severity(severity):
        return "❌ Error: Invalid severity. Must be one of: critical, major, warning"
    
    # Use provided timestamp or generate current one
    alert_timestamp = timestamp.strip() if timestamp.strip() else format_timestamp()
    
    # Prepare alert data
    alert_data = {
        "location": location.strip(),
        "severity": severity.strip(),
        "message": message.strip(),
        "source": source.strip(),
        "timestamp": alert_timestamp
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{ALERTHARVEST_URL}/api/create_alert/",
                json=alert_data,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get("status") == "success":
                return f"""✅ Alert Created Successfully
📍 Location: {location}
⚠️ Severity: {severity}
💬 Message: {message}
🔗 Source: {source}
⏱️ Timestamp: {alert_timestamp}"""
            else:
                return f"❌ Error: {result.get('message', 'Unknown error')}"
                
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error: {e.response.status_code}")
        return f"❌ API Error: HTTP {e.response.status_code}"
    except Exception as e:
        logger.error(f"Error creating alert: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def acknowledge_alert(alert_id: str = "") -> str:
    """Acknowledge a specific alert by its ID to mark it as seen."""
    logger.info(f"Acknowledging alert: {alert_id}")
    
    if not alert_id.strip():
        return "❌ Error: Alert ID is required"
    
    # Validate alert_id is numeric
    try:
        alert_id_int = int(alert_id.strip())
    except ValueError:
        return f"❌ Error: Alert ID must be a number, got: {alert_id}"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{ALERTHARVEST_URL}/api/acknowledge_alert/{alert_id_int}",
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get("status") == "success":
                return f"✅ Alert #{alert_id_int} acknowledged successfully"
            else:
                return f"❌ Error: {result.get('message', 'Unknown error')}"
                
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error: {e.response.status_code}")
        return f"❌ API Error: HTTP {e.response.status_code} - Alert may not exist"
    except Exception as e:
        logger.error(f"Error acknowledging alert: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def acknowledge_alerts_bulk(alert_ids: str = "") -> str:
    """Acknowledge multiple alerts at once by providing comma-separated alert IDs."""
    logger.info(f"Acknowledging alerts in bulk: {alert_ids}")
    
    if not alert_ids.strip():
        return "❌ Error: Alert IDs are required (comma-separated)"
    
    # Parse comma-separated IDs
    try:
        id_list = [int(id.strip()) for id in alert_ids.split(",") if id.strip()]
        if not id_list:
            return "❌ Error: No valid alert IDs provided"
    except ValueError:
        return "❌ Error: All alert IDs must be numbers"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{ALERTHARVEST_URL}/api/acknowledge_alerts_bulk/",
                json={"alert_ids": id_list},
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get("status") == "success":
                return f"✅ {len(id_list)} alerts acknowledged successfully: {id_list}"
            else:
                return f"❌ Error: {result.get('message', 'Unknown error')}"
                
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error: {e.response.status_code}")
        return f"❌ API Error: HTTP {e.response.status_code}"
    except Exception as e:
        logger.error(f"Error acknowledging alerts in bulk: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def unacknowledge_alert(alert_id: str = "") -> str:
    """Unacknowledge a specific alert by its ID to mark it as unread again."""
    logger.info(f"Unacknowledging alert: {alert_id}")
    
    if not alert_id.strip():
        return "❌ Error: Alert ID is required"
    
    # Validate alert_id is numeric
    try:
        alert_id_int = int(alert_id.strip())
    except ValueError:
        return f"❌ Error: Alert ID must be a number, got: {alert_id}"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{ALERTHARVEST_URL}/api/unacknowledge_alert/{alert_id_int}",
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get("status") == "success":
                return f"✅ Alert #{alert_id_int} unacknowledged successfully"
            else:
                return f"❌ Error: {result.get('message', 'Unknown error')}"
                
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error: {e.response.status_code}")
        return f"❌ API Error: HTTP {e.response.status_code} - Alert may not exist"
    except Exception as e:
        logger.error(f"Error unacknowledging alert: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def close_alert(alert_id: str = "") -> str:
    """Close a specific alert by its ID to mark it as resolved."""
    logger.info(f"Closing alert: {alert_id}")
    
    if not alert_id.strip():
        return "❌ Error: Alert ID is required"
    
    # Validate alert_id is numeric
    try:
        alert_id_int = int(alert_id.strip())
    except ValueError:
        return f"❌ Error: Alert ID must be a number, got: {alert_id}"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{ALERTHARVEST_URL}/api/close_alert/{alert_id_int}",
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get("status") == "success":
                return f"✅ Alert #{alert_id_int} closed successfully"
            else:
                return f"❌ Error: {result.get('message', 'Unknown error')}"
                
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error: {e.response.status_code}")
        return f"❌ API Error: HTTP {e.response.status_code} - Alert may not exist"
    except Exception as e:
        logger.error(f"Error closing alert: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def close_alerts_bulk(alert_ids: str = "") -> str:
    """Close multiple alerts at once by providing comma-separated alert IDs."""
    logger.info(f"Closing alerts in bulk: {alert_ids}")
    
    if not alert_ids.strip():
        return "❌ Error: Alert IDs are required (comma-separated)"
    
    # Parse comma-separated IDs
    try:
        id_list = [int(id.strip()) for id in alert_ids.split(",") if id.strip()]
        if not id_list:
            return "❌ Error: No valid alert IDs provided"
    except ValueError:
        return "❌ Error: All alert IDs must be numbers"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{ALERTHARVEST_URL}/api/close_alerts_bulk/",
                json={"alert_ids": id_list},
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get("status") == "success":
                return f"✅ {len(id_list)} alerts closed successfully: {id_list}"
            else:
                return f"❌ Error: {result.get('message', 'Unknown error')}"
                
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error: {e.response.status_code}")
        return f"❌ API Error: HTTP {e.response.status_code}"
    except Exception as e:
        logger.error(f"Error closing alerts in bulk: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def close_expired_alerts() -> str:
    """Close all expired alerts automatically based on AlertHarvest's expiration rules."""
    logger.info("Closing expired alerts")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{ALERTHARVEST_URL}/api/close_expired_alerts/",
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get("status") == "success":
                return f"✅ {result.get('message', 'Expired alerts closed successfully')}"
            else:
                return f"❌ Error: {result.get('message', 'Unknown error')}"
                
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error: {e.response.status_code}")
        return f"❌ API Error: HTTP {e.response.status_code}"
    except Exception as e:
        logger.error(f"Error closing expired alerts: {e}")
        return f"❌ Error: {str(e)}"

# === SERVER STARTUP ===
if __name__ == "__main__":
    logger.info("Starting AlertHarvest MCP server...")
    
    # Log configuration
    logger.info(f"AlertHarvest URL: {ALERTHARVEST_URL}")
    
    try:
        mcp.run(transport='stdio')
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)
