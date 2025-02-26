#!/usr/bin/env python3
"""
MCP Server Example

This example demonstrates how to use the server configuration manager
to configure and start an MCP server.
"""

import os
import sys
import asyncio
import logging
from typing import Dict, Any

# Add parent directory to path to import tools
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.server_config_manager import get_server_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Mock classes for demonstration (similar to the test classes)
class MCPServer:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.middleware = []
        self.routes = {}
        self.status = "initialized"
        logger.info(f"Initialized MCPServer with config: {config}")
        
    def add_middleware(self, middleware):
        self.middleware.append(middleware)
        logger.info(f"Added middleware: {middleware.__class__.__name__}")
        
    def add_route(self, path: str, handler):
        self.routes[path] = handler
        logger.info(f"Added route: {path}")
        
    def is_configured(self) -> bool:
        return all(k in self.config for k in ["host", "port", "workers", "timeout"])
        
    def get_status(self) -> str:
        return self.status
        
    async def start(self):
        self.status = "running"
        host = self.config.get("host", "localhost")
        port = self.config.get("port", 8000)
        logger.info(f"Server started on {host}:{port}")
        
    async def shutdown(self):
        self.status = "stopped"
        logger.info("Server shutdown")

class SecurityMiddleware:
    def __init__(self, **kwargs):
        self.enabled = kwargs.get("enabled", True)
        self.rate_limit = kwargs.get("rate_limit", {})
        self.allowed_hosts = kwargs.get("allowed_hosts", [])
        logger.info(f"Initialized SecurityMiddleware: enabled={self.enabled}, rate_limit={self.rate_limit}, allowed_hosts={self.allowed_hosts}")

class MetricsMiddleware:
    def __init__(self, **kwargs):
        self.enabled = kwargs.get("enabled", True)
        self.enable_timing = kwargs.get("enable_timing", False)
        self.track_endpoints = kwargs.get("track_endpoints", False)
        self.metrics_path = kwargs.get("metrics_path", "/metrics")
        self.metrics = {}
        logger.info(f"Initialized MetricsMiddleware: enabled={self.enabled}, enable_timing={self.enable_timing}, track_endpoints={self.track_endpoints}")

async def health_check(request):
    """Simple health check endpoint."""
    return {"status": "healthy"}

async def echo(request):
    """Echo endpoint that returns the request data."""
    return {"echo": request.get("data", {})}

async def main():
    """Main function to demonstrate server configuration and startup."""
    # Get environment from command line or use default
    import argparse
    parser = argparse.ArgumentParser(description='MCP Server Example')
    parser.add_argument('--env', default='development', help='Environment (development, test, staging, production)')
    parser.add_argument('--server', default='main', help='Server name (main, secondary, analytics, etc.)')
    args = parser.parse_args()
    
    try:
        # Get server configuration for the specified environment
        config = get_server_config(args.env, args.server)
        logger.info(f"Using server configuration for {args.server} in {args.env} environment")
        
        # Create server instance
        server = MCPServer(config)
        
        # Add middleware from configuration
        for middleware_config in config.get("middleware", []):
            for middleware_name, middleware_options in middleware_config.items():
                if middleware_name == "SecurityMiddleware":
                    server.add_middleware(SecurityMiddleware(**middleware_options))
                elif middleware_name == "MetricsMiddleware":
                    server.add_middleware(MetricsMiddleware(**middleware_options))
        
        # Add routes
        server.add_route("/health", health_check)
        server.add_route("/echo", echo)
        
        # Start server
        if server.is_configured():
            await server.start()
            
            # In a real application, we would keep the server running
            # For this example, we'll just wait a bit and then shut down
            logger.info("Server running. Press Ctrl+C to stop...")
            try:
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                logger.info("Received shutdown signal")
            finally:
                await server.shutdown()
        else:
            logger.error("Server is not properly configured")
            
    except Exception as e:
        logger.error(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 