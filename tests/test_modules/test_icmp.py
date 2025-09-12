"""Tests for ICMP module."""

from unittest.mock import patch

from mcpcap.core.config import Config
from mcpcap.modules.icmp import ICMPModule


class TestICMPModule:
    """Test ICMP module functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        config = Config(modules=["icmp"], max_packets=None)
        self.icmp_module = ICMPModule(config)

    def test_protocol_name(self):
        """Test protocol name property."""
        assert self.icmp_module.protocol_name == "ICMP"

    @patch("mcpcap.modules.icmp.rdpcap")
    def test_analyze_icmp_packets_no_packets(self, mock_rdpcap):
        """Test analysis with no ICMP packets."""
        # Mock empty packet capture
        mock_rdpcap.return_value = []

        with patch("os.path.exists", return_value=True):
            result = self.icmp_module.analyze_icmp_packets("test.pcap")

        assert result["icmp_packets_found"] == 0
        assert "No ICMP packets found" in result["message"]

    def test_generate_statistics_empty(self):
        """Test statistics generation with empty packet list."""
        stats = self.icmp_module._generate_statistics([])

        assert stats["unique_sources_count"] == 0
        assert stats["unique_destinations_count"] == 0
        assert stats["echo_sessions"] == 0

    def test_generate_statistics_with_packets(self):
        """Test statistics generation with sample packets."""
        packets = [
            {
                "icmp_type_name": "Echo Request",
                "icmp_type": 8,
                "icmp_id": 123,
                "src_ip": "192.168.1.100",
                "dst_ip": "8.8.8.8",
            },
            {
                "icmp_type_name": "Echo Reply",
                "icmp_type": 0,
                "icmp_id": 123,
                "src_ip": "8.8.8.8",
                "dst_ip": "192.168.1.100",
            },
            {
                "icmp_type_name": "Destination Unreachable",
                "icmp_type": 3,
                "src_ip": "192.168.1.1",
                "dst_ip": "192.168.1.100",
            },
        ]

        stats = self.icmp_module._generate_statistics(packets)

        assert stats["icmp_type_counts"]["Echo Request"] == 1
        assert stats["icmp_type_counts"]["Echo Reply"] == 1
        assert stats["icmp_type_counts"]["Destination Unreachable"] == 1
        assert stats["unique_sources_count"] == 3  # 192.168.1.100, 8.8.8.8, 192.168.1.1
        assert stats["unique_destinations_count"] == 2  # 8.8.8.8, 192.168.1.100
        assert stats["echo_sessions"] == 1
        assert stats["echo_pairs"][123]["requests"] == 1
        assert stats["echo_pairs"][123]["replies"] == 1
