# MCP Client Integration

Learn how to integrate mcpcap with different MCP (Model Context Protocol) clients.

## What is MCP?

The Model Context Protocol (MCP) enables LLMs to securely access external resources and tools. mcpcap implements an MCP server that provides network protocol analysis capabilities (DNS, DHCP, and more) to any compatible MCP client.

## Available MCP Clients

### Claude Desktop

**Best for**: End users who want AI-powered network analysis

Claude Desktop is Anthropic's official desktop application with built-in MCP support.

#### Setup

1. Install Claude Desktop from [claude.ai](https://claude.ai)
2. Open Claude Desktop settings (Cmd/Ctrl + ,)
3. Add mcpcap to your MCP configuration:

```json
{
  "mcpServers": {
    "mcpcap": {
      "command": "mcpcap",
      "args": []
    }
  }
}
```

4. Restart Claude Desktop
5. Start a conversation and you'll see mcpcap tools available

#### Usage Tips

- Ask Claude to analyze DNS traffic: `analyze_dns_packets("/path/to/malware.pcap")`
- Request security-focused analysis: "Use security_analysis prompt to examine this DNS data"
- Get troubleshooting help: "Use network_troubleshooting prompt to diagnose DNS issues"
- Analyze DHCP traffic: `analyze_dhcp_packets("/path/to/network.pcap")`

### MCP Inspector

**Best for**: Developers and technical users who want to test tools directly

MCP Inspector provides a web-based interface for testing MCP servers.

#### Setup

```bash
# Install globally
npm install -g @modelcontextprotocol/inspector

# Run with mcpcap
npx @modelcontextprotocol/inspector mcpcap
```

#### Features

- Interactive tool testing
- Real-time parameter input
- JSON response viewing
- Resource and prompt exploration

### Custom Python Client

**Best for**: Developers integrating mcpcap into applications

Build your own MCP client using the Python MCP library.

#### Example Implementation

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def analyze_dns():
    # Connect to mcpcap server
    server_params = StdioServerParameters(
        command="mcpcap",
        args=[]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            print("Available tools:", [tool.name for tool in tools.tools])
            
            # Call a tool
            result = await session.call_tool(
                "analyze_dns_packets",
                arguments={"pcap_file": "example.pcap"}
            )
            
            print("Analysis result:", result.content)

# Run the analysis
asyncio.run(analyze_dns())
```

## Available Tools

### `list_pcap_files`

Lists all PCAP files in the configured directory.

**Parameters**: None

**Returns**: List of available .pcap and .pcapng files

### `analyze_dns_packets`

Analyzes DNS packets in a PCAP file.

**Parameters**:
- `pcap_file` (optional): Filename to analyze (defaults to first available file)

**Returns**: Structured JSON with DNS packet details and statistics

### `analyze_dhcp_packets`

Analyzes DHCP packets in a PCAP file.

**Parameters**:
- `pcap_file` (optional): Filename to analyze (defaults to first available file)

**Returns**: Structured JSON with DHCP packet details including:
- Complete DHCP transactions (DISCOVER → OFFER → REQUEST → ACK)
- Client and server identification (MAC addresses, hostnames)
- IP address assignments and lease information
- DHCP options and configurations
- Transaction timing and statistics

## Available Prompts

### DNS Analysis Prompts

- `security_analysis`: Security-focused DNS analysis guidance
- `network_troubleshooting`: Network performance troubleshooting
- `forensic_investigation`: Digital forensics approach

### DHCP Analysis Prompts

- `dhcp_network_analysis`: Network administration and IP management analysis
- `dhcp_security_analysis`: Security threats and rogue DHCP server detection
- `dhcp_forensic_investigation`: Forensic analysis of DHCP transactions and timeline

## Configuration Options

### Server Configuration

```bash
# Local directory
mcpcap /path/to/pcaps

# Local file
mcpcap /path/to/specific.pcap

# Remote file
mcpcap https://example.com/capture.pcap

# With analysis options
mcpcap /path/to/pcaps --max-packets 1000 --modules dns,dhcp
```

### Client Configuration Examples

#### Claude Desktop (Extended)

```json
{
  "mcpServers": {
    "mcpcap-local-file": {
      "command": "mcpcap",
      "args": ["--pcap-path", "/path/to/specific.pcap", "--max-packets", "500"]
    },
    "mcpcap-production": {
      "command": "mcpcap",
      "args": ["--pcap-path", "/production/captures", "--modules", "dns,dhcp"],
      "env": {
        "LOG_LEVEL": "INFO"
      }
    },
    "mcpcap-remote": {
      "command": "mcpcap", 
      "args": ["--pcap-url", "https://example.com/samples/dns.cap"]
    }
  }
}
```

#### Environment Variables

```bash
# Set logging level
export LOG_LEVEL=DEBUG

# Set default PCAP path
export mcpcap_PCAP_PATH=/default/path
```

## Best Practices

### Security

- Never point mcpcap at directories with sensitive captures
- Use read-only permissions for PCAP directories when possible
- Be cautious with captures containing personal information

### Performance

- Use specific filenames instead of analyzing all files at once
- Consider splitting large PCAP files for better performance
- Monitor memory usage with very large captures

### Organization

- Organize PCAP files by date, source, or investigation
- Use descriptive filenames: `malware-sample-2024-01-15.pcap`
- Keep separate directories for different analysis projects

## Troubleshooting

### Common Issues

**Tool not available in Claude Desktop**
- Check MCP configuration syntax
- Restart Claude Desktop after configuration changes
- Verify mcpcap is installed and accessible

**Server connection failed**
- Ensure PCAP directory exists and is readable
- Check that mcpcap command works from terminal
- Verify no other processes are using the same resources

**Empty results**
- Confirm PCAP files contain expected traffic (DNS on `port 53`, DHCP on `port 67/68`)
- Check file extensions are `.pcap` or `.pcapng`
- Verify files aren't corrupted with `file` command
- Ensure protocol modules are properly configured (`--modules dns,dhcp`)

**Performance issues**
- Use smaller PCAP files for initial testing
- Consider filtering large captures before analysis
- Monitor system resources during analysis

## Integration Examples

### Security Operations Center (SOC)

```json
{
  "mcpServers": {
    "mcpcap-incident": {
      "command": "mcpcap",
      "args": ["--pcap-path", "/incidents/current"]
    }
  }
}
```

### Network Troubleshooting

```json
{
  "mcpServers": {
    "mcpcap-network": {
      "command": "mcpcap",
      "args": ["--pcap-path", "/network/diagnostics"]
    }
  }
}
```

### Research and Development

```json
{
  "mcpServers": {
    "mcpcap-research": {
      "command": "mcpcap",
      "args": ["--pcap-path", "/research/samples"]
    }
  }
}
```