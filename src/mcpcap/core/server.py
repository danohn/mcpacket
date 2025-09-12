"""MCP server setup and configuration."""

from fastmcp import FastMCP

from ..modules.dhcp import DHCPModule
from ..modules.dns import DNSModule
from .config import Config


class MCPServer:
    """MCP server for PCAP analysis."""

    def __init__(self, config: Config):
        """Initialize MCP server.

        Args:
            config: Configuration instance
        """
        self.config = config
        self.mcp = FastMCP("mcpcap")

        # Initialize modules based on configuration
        self.modules = {}
        if "dns" in self.config.modules:
            self.modules["dns"] = DNSModule(config)
        if "dhcp" in self.config.modules:
            self.modules["dhcp"] = DHCPModule(config)

        # Register tools
        self._register_tools()

        # Setup prompts
        for module in self.modules.values():
            module.setup_prompts(self.mcp)

    def _register_tools(self) -> None:
        """Register all available tools with the MCP server."""
        # Register tools for each loaded module
        for module_name, module in self.modules.items():
            if module_name == "dns":
                self.mcp.tool(module.analyze_dns_packets)
            elif module_name == "dhcp":
                self.mcp.tool(module.analyze_dhcp_packets)

    def run(self) -> None:
        """Start the MCP server."""
        import sys

        # Log to stderr to avoid breaking MCP JSON-RPC protocol
        enabled_modules = ", ".join(self.config.modules)
        print(f"Starting mcpcap MCP server with modules: {enabled_modules}", file=sys.stderr)

        self.mcp.run()
