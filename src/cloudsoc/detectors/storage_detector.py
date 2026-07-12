"""CloudSOC Storage Detector"""

from typing import Dict

from cloudsoc.core.logger import logger


class StorageDetector:
    """Detects storage usage issues."""

    def __init__(self, warning: float = 80.0, critical: float = 95.0) -> None:
        self.warning = float(warning)
        self.critical = float(critical)

    def _parse_size(self, size_str: str) -> float:
        """Parse a human-readable size (e.g. '10 GiB') into bytes.

        Supports both binary (KiB, MiB, GiB, TiB) and SI (KB, MB, GB, TB).
        """
        parts = size_str.strip().split()
        if not parts:
            raise ValueError("empty size string")

        # If only a number is given, assume bytes
        if len(parts) == 1:
            value = float(parts[0])
            unit = "B"
        else:
            value = float(parts[0])
            unit = parts[1]

        units = {
            "B": 1,
            "KB": 10**3,
            "KIB": 1024,
            "MB": 10**6,
            "MIB": 1024**2,
            "GB": 10**9,
            "GIB": 1024**3,
            "TB": 10**12,
            "TIB": 1024**4,
        }

        key = unit.upper()
        if key not in units:
            # allow common variations like 'KiB', 'GiB' in different cases
            key = key.replace("IB", "IB")

        if key not in units:
            raise ValueError(f"unknown unit: {unit}")

        return value * units[key]

    def check(self, cloud: Dict) -> None:
        """Check storage usage and log an event if thresholds exceeded."""

        service = cloud.get("service", "unknown")
        try:
            used = cloud["used"]
            total = cloud["total"]

            used_bytes = self._parse_size(used)
            total_bytes = self._parse_size(total)

            if total_bytes <= 0:
                logger.error(service, "Storage total size is zero or invalid")
                return

            percent = (used_bytes / total_bytes) * 100

        except Exception as exc:
            logger.error(service, f"Storage check failed: {exc}")
            return

        if percent >= self.critical:
            logger.critical(service, f"Storage Critical ({percent:.1f}%)")
        elif percent >= self.warning:
            logger.warning(service, f"Storage Warning ({percent:.1f}%)")
        else:
            logger.success(service, f"Storage Healthy ({percent:.1f}%)")