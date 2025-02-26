import pytest
import pytest_asyncio
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import aiohttp
import json
import time

# Mock classes for testing
class MCPServer:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.middleware = []
        self.routes = {}
        self.status = "initialized"
        
    def add_middleware(self, middleware):
        self.middleware.append(middleware)
        
    def add_route(self, path: str, handler):
        self.routes[path] = handler
        
    def is_configured(self) -> bool:
        return all(k in self.config for k in ["host", "port", "workers", "timeout"])
        
    def get_status(self) -> str:
        return self.status
        
    async def start(self):
        self.status = "running"
        
    async def shutdown(self):
        self.status = "stopped"

class SecurityMiddleware:
    def __init__(self):
        self.enabled = True

class MetricsMiddleware:
    def __init__(self):
        self.metrics = {}

@pytest.fixture
def mock_config() -> Dict[str, Any]:
    return {
        "host": "localhost",
        "port": 8000,
        "workers": 4,
        "timeout": 30,
        "max_requests": 1000,
        "keepalive": 5,
        "security": {
            "ssl_enabled": False,
            "allowed_origins": ["http://localhost:3000"],
            "rate_limit": {
                "requests": 100,
                "period": 60
            }
        }
    }

@pytest.fixture
def mock_log_dir(tmp_path: Path) -> Path:
    log_dir = tmp_path / ".cursor" / "logs" / "mcp_server"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir

@pytest_asyncio.fixture
async def server(mock_config: Dict[str, Any]) -> MCPServer:
    server = MCPServer(mock_config)
    await server.start()
    try:
        yield server
    finally:
        await server.shutdown()

@pytest.mark.asyncio
async def test_server_initialization(mock_config: Dict[str, Any]):
    """Test that the server initializes correctly with given configuration."""
    server = MCPServer(mock_config)
    
    assert server.is_configured()
    assert server.get_status() == "initialized"
    assert server.config["host"] == "localhost"
    assert server.config["port"] == 8000

@pytest.mark.asyncio
async def test_server_middleware(server: MCPServer):
    """Test that middleware can be added to the server."""
    security = SecurityMiddleware()
    metrics = MetricsMiddleware()
    
    server.add_middleware(security)
    server.add_middleware(metrics)
    
    assert len(server.middleware) == 2
    assert isinstance(server.middleware[0], SecurityMiddleware)
    assert isinstance(server.middleware[1], MetricsMiddleware)

@pytest.mark.asyncio
async def test_server_lifecycle(server: MCPServer):
    """Test server startup and shutdown."""
    assert server.get_status() == "running"
    
    await server.shutdown()
    assert server.get_status() == "stopped"

@pytest.mark.asyncio
async def test_route_registration(server: MCPServer):
    """Test that routes can be registered with the server."""
    async def test_handler(request):
        return {"status": "ok"}
    
    server.add_route("/api/test", test_handler)
    assert "/api/test" in server.routes
    assert server.routes["/api/test"] == test_handler

@pytest.mark.asyncio
async def test_server_config_validation(mock_config: Dict[str, Any]):
    """Test that server configuration is properly validated."""
    # Test with valid config
    server = MCPServer(mock_config)
    assert server.is_configured()
    
    # Test with missing required fields
    invalid_config = {"host": "localhost"}  # Missing other required fields
    server_invalid = MCPServer(invalid_config)
    assert not server_invalid.is_configured(), "Server should not be configured with missing required fields"

@pytest.mark.asyncio
async def test_security_middleware(server: MCPServer):
    """Test that security middleware is properly configured."""
    security = SecurityMiddleware()
    server.add_middleware(security)
    
    assert any(isinstance(m, SecurityMiddleware) for m in server.middleware)
    assert server.middleware[0].enabled

@pytest.mark.asyncio
async def test_metrics_middleware(server: MCPServer):
    """Test that metrics middleware is properly configured."""
    metrics = MetricsMiddleware()
    server.add_middleware(metrics)
    
    assert any(isinstance(m, MetricsMiddleware) for m in server.middleware)
    assert isinstance(metrics.metrics, dict)

@pytest.mark.asyncio
async def test_generate_server_report(mock_log_dir: Path, server: MCPServer):
    """Test generation of server status report."""
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    report_path = mock_log_dir / f"server_report_{timestamp}.txt"
    
    # Generate report
    with open(report_path, "w") as f:
        f.write(f"Server Status Report - {timestamp}\n")
        f.write(f"Status: {server.get_status()}\n")
        f.write(f"Configuration:\n")
        for key, value in server.config.items():
            f.write(f"  {key}: {value}\n")
        f.write(f"Middleware Count: {len(server.middleware)}\n")
        f.write(f"Routes Count: {len(server.routes)}\n")
    
    assert report_path.exists()
    assert report_path.is_file()
    
    # Verify report content
    content = report_path.read_text()
    assert "Server Status Report" in content
    assert f"Status: {server.get_status()}" in content
    assert "Configuration:" in content
    assert "Middleware Count:" in content
    assert "Routes Count:" in content

@pytest.mark.asyncio
async def test_server_error_handling(server: MCPServer):
    """Test server error handling capabilities."""
    async def error_handler(request):
        raise ValueError("Test error")
    
    server.add_route("/api/error", error_handler)
    
    try:
        await server.routes["/api/error"](None)
        pytest.fail("Should have raised an error")
    except ValueError as e:
        assert str(e) == "Test error"

@pytest.mark.asyncio
async def test_server_performance(server: MCPServer):
    """Test server performance metrics collection."""
    metrics = MetricsMiddleware()
    server.add_middleware(metrics)
    
    # Simulate requests with unique timestamps to avoid overwriting
    for i in range(5):
        metrics.metrics[f"2025-02-26T07:14:46.{495647+i}"] = {
            "response_time": 0.1,
            "status_code": 200
        }
        time.sleep(0.001)  # Ensure unique timestamps
    
    assert len(metrics.metrics) == 5
    assert all(isinstance(m["response_time"], float) for m in metrics.metrics.values())
    assert all(m["status_code"] == 200 for m in metrics.metrics.values()) 