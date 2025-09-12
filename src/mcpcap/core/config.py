"""Configuration management for mcpcap."""


class Config:
    """Configuration management for mcpcap server."""

    def __init__(
        self,
        modules: list[str] | None = None,
        protocols: list[str] | None = None,
        max_packets: int | None = None,
    ):
        """Initialize configuration.

        Args:
            modules: List of modules to load
            protocols: List of protocols to analyze
            max_packets: Maximum number of packets to analyze per file
        """
        self.modules = modules or ["dns", "dhcp"]
        self.protocols = protocols or ["dns", "dhcp"]
        self.max_packets = max_packets

        self._validate_configuration()

    def _validate_configuration(self) -> None:
        """Validate the configuration parameters."""
        if self.max_packets is not None and self.max_packets <= 0:
            raise ValueError("max_packets must be a positive integer")
