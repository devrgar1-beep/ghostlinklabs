#!/usr/bin/env python3
"""
GhostLink Network Monitor
Monitors the sovereign Eero 7 network and AI infrastructure health
"""

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict

import aiohttp


class GhostLinkNetworkMonitor:
    """Monitor the sovereign GhostLink network infrastructure"""

    def __init__(self):
        self.network_config = {
            "gateway": "192.168.1.1",
            "services": {
                "ghostlink": "192.168.1.100:8000",
                "redis": "192.168.1.101:6379",
                "postgres": "192.168.1.102:5432",
                "ollama": "192.168.1.103:11434",
                "prometheus": "192.168.1.104:9090",
                "grafana": "192.168.1.105:3000",
                "nginx": "192.168.1.106:80",
            },
        }
        self.monitor_log = Path("logs/network_monitor.log")

    async def check_service_health(self, service_name: str, endpoint: str) -> Dict:
        """Check health of a specific service"""
        try:
            if ":" not in endpoint:
                # Ping check for services without HTTP ports
                result = await asyncio.create_subprocess_exec(
                    "ping",
                    "-c",
                    "1",
                    "-W",
                    "1",
                    endpoint.split(":")[0],
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                await result.wait()
                status = result.returncode == 0
                return {
                    "service": service_name,
                    "endpoint": endpoint,
                    "status": "healthy" if status else "unreachable",
                    "response_time": None,
                    "timestamp": datetime.now().isoformat(),
                }

            # HTTP health check
            url = f"http://{endpoint}/health"
            start_time = time.time()

            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
                async with session.get(url) as response:
                    response_time = time.time() - start_time
                    status = "healthy" if response.status == 200 else "unhealthy"
                    return {
                        "service": service_name,
                        "endpoint": endpoint,
                        "status": status,
                        "response_time": round(response_time * 1000, 2),  # ms
                        "http_status": response.status,
                        "timestamp": datetime.now().isoformat(),
                    }

        except Exception as e:
            return {
                "service": service_name,
                "endpoint": endpoint,
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    async def check_network_connectivity(self) -> Dict:
        """Check overall network connectivity"""
        try:
            # Check gateway
            result = await asyncio.create_subprocess_exec(
                "ping",
                "-c",
                "3",
                self.network_config["gateway"],
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await result.wait()

            # Get network info
            network_info = {
                "gateway_reachable": result.returncode == 0,
                "timestamp": datetime.now().isoformat(),
            }

            # Check internet connectivity
            try:
                async with aiohttp.ClientSession(
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as session:
                    async with session.get("https://httpbin.org/ip") as response:
                        network_info["internet_connected"] = response.status == 200
            except:
                network_info["internet_connected"] = False

            return network_info

        except Exception as e:
            return {"error": str(e), "timestamp": datetime.now().isoformat()}

    async def monitor_network(self) -> None:
        """Main monitoring loop"""
        print("🔗 GhostLink Network Monitor Started")
        print("Monitoring sovereign Eero 7 infrastructure...")
        print("=" * 50)

        while True:
            try:
                # Check network connectivity
                network_status = await self.check_network_connectivity()

                # Check all services
                service_checks = []
                for service, endpoint in self.network_config["services"].items():
                    status = await self.check_service_health(service, endpoint)
                    service_checks.append(status)

                    # Print status
                    status_emoji = (
                        "✅"
                        if status["status"] == "healthy"
                        else "❌" if status["status"] == "unreachable" else "⚠️"
                    )
                    print(f"{status_emoji} {service}: {status['status']}")

                # Network status
                gateway_emoji = "✅" if network_status.get("gateway_reachable") else "❌"
                internet_emoji = "✅" if network_status.get("internet_connected") else "❌"
                print(
                    f"{gateway_emoji} Gateway: {'reachable' if network_status.get('gateway_reachable') else 'unreachable'}"
                )
                print(
                    f"{internet_emoji} Internet: {'connected' if network_status.get('internet_connected') else 'disconnected'}"
                )

                # Save to log
                log_entry = {
                    "timestamp": datetime.now().isoformat(),
                    "network": network_status,
                    "services": service_checks,
                }

                with open(self.monitor_log, "a") as f:
                    f.write(json.dumps(log_entry) + "\n")

                print(f"📊 Status logged to {self.monitor_log}")
                print("-" * 30)

            except Exception as e:
                print(f"❌ Monitor error: {e}")

            await asyncio.sleep(60)  # Check every minute

    async def run_diagnostics(self) -> None:
        """Run comprehensive network diagnostics"""
        print("🔍 Running GhostLink Network Diagnostics")
        print("=" * 50)

        # Network info
        print("📡 Network Information:")
        try:
            result = await asyncio.create_subprocess_exec(
                "ip", "route", "show", stdout=asyncio.subprocess.PIPE
            )
            stdout, _ = await result.communicate()
            print(stdout.decode().strip())
        except:
            print("Could not get network routes")

        print("\n🔗 Service Connectivity:")
        for service, endpoint in self.network_config["services"].items():
            status = await self.check_service_health(service, endpoint)
            print(f"  {service}: {status['status']} ({endpoint})")

        print("\n✅ Diagnostics complete")


async def main():
    """Main entry point"""
    monitor = GhostLinkNetworkMonitor()

    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "diagnostics":
        await monitor.run_diagnostics()
    else:
        await monitor.monitor_network()


if __name__ == "__main__":
    asyncio.run(main())
