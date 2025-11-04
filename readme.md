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
