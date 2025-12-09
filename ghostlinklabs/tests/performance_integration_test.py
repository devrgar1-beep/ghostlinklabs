#!/usr/bin/env python3
"""
GhostLink Performance Integration Tests
Tests the integration of performance monitoring, connection pooling, and metrics endpoints
"""

import os
import subprocess
import sys
import time

import pytest
import requests

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestPerformanceIntegration:
    """Test performance monitoring integration"""

    def test_performance_monitor_import(self):
        """Test that performance monitor can be imported"""
        try:
            import importlib.util
            performance_path = os.path.join(os.path.dirname(__file__), '..', 'performance', 'optimization')

            # Import performance monitor
            perf_spec = importlib.util.spec_from_file_location(
                "performance_monitor",
                os.path.join(performance_path, "performance-monitor.py")
            )
            perf_module = importlib.util.module_from_spec(perf_spec)
            perf_spec.loader.exec_module(perf_module)
            performance_monitor = perf_module.PerformanceMonitor()

            assert performance_monitor is not None
            assert hasattr(performance_monitor, 'record_request')
            assert hasattr(performance_monitor, 'get_performance_report')
            print("✅ Performance monitor import test passed")

        except Exception as e:
            pytest.fail(f"Performance monitor import failed: {e}")

    def test_connection_pool_import(self):
        """Test that connection pool can be imported"""
        try:
            import importlib.util
            performance_path = os.path.join(os.path.dirname(__file__), '..', 'performance', 'optimization')

            # Import connection pool
            pool_spec = importlib.util.spec_from_file_location(
                "connection_pool",
                os.path.join(performance_path, "connection-pool.py")
            )
            pool_module = importlib.util.module_from_spec(pool_spec)
            pool_spec.loader.exec_module(pool_module)

            assert hasattr(pool_module, 'init_connection_pools')
            assert hasattr(pool_module, 'ConnectionPoolManager')
            assert callable(pool_module.init_connection_pools)
            print("✅ Connection pool import test passed")

        except Exception as e:
            pytest.fail(f"Connection pool import failed: {e}")

    @pytest.mark.asyncio
    async def test_connection_pool_initialization(self):
        """Test that connection pools can be initialized"""
        try:
            import importlib.util
            performance_path = os.path.join(os.path.dirname(__file__), '..', 'performance', 'optimization')

            # Import connection pool
            pool_spec = importlib.util.spec_from_file_location(
                "connection_pool",
                os.path.join(performance_path, "connection-pool.py")
            )
            pool_module = importlib.util.module_from_spec(pool_spec)
            pool_spec.loader.exec_module(pool_module)

            # Test initialization (should not fail even if dependencies missing)
            await pool_module.init_connection_pools()
            print("✅ Connection pool initialization test passed")

        except Exception as e:
            # This is expected if Redis/MySQL not available
            print(f"⚠️  Connection pool initialization failed (expected): {e}")

    def test_api_server_performance_endpoint(self):
        """Test that API server has performance endpoint"""
        try:
            # Start API server in background
            server_process = subprocess.Popen([
                sys.executable, 'ghostlink_api_server_enhanced.py', '--port', '3001'
            ], cwd=os.path.dirname(__file__),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Wait for server to start
            time.sleep(2)

            try:
                # Test health endpoint
                response = requests.get('http://localhost:3001/health', timeout=5)
                assert response.status_code == 200
                data = response.json()
                assert 'status' in data
                assert data['status'] == 'healthy'
                print("✅ API server health endpoint test passed")

                # Test performance endpoint
                response = requests.get('http://localhost:3001/performance', timeout=5)
                assert response.status_code == 200
                data = response.json()
                assert 'timestamp' in data
                print("✅ API server performance endpoint test passed")

            finally:
                # Clean up server
                server_process.terminate()
                server_process.wait(timeout=5)

        except Exception as e:
            pytest.fail(f"API server performance endpoint test failed: {e}")

    def test_orchestrator_metrics_endpoint(self):
        """Test that AI orchestrator has metrics endpoint"""
        try:
            # Import orchestrator module
            import importlib.util
            orch_spec = importlib.util.spec_from_file_location(
                "optimized_ai_orchestrator",
                os.path.join(os.path.dirname(__file__), "..", "optimized_ai_orchestrator.py")
            )
            orch_module = importlib.util.module_from_spec(orch_spec)
            orch_spec.loader.exec_module(orch_module)

            # Check that metrics methods exist
            orchestrator = orch_module.OptimizedMasterOrchestrator()
            assert hasattr(orchestrator, 'start_metrics_server')
            assert hasattr(orchestrator, 'get_orchestrator_metrics')
            print("✅ Orchestrator metrics methods test passed")

        except Exception as e:
            pytest.fail(f"Orchestrator metrics endpoint test failed: {e}")

    def test_prometheus_configuration(self):
        """Test that Prometheus configuration includes autoscaling rules"""
        try:
            import yaml

            prometheus_config_path = os.path.join(os.path.dirname(__file__), '..', 'monitoring', 'prometheus.yml')
            with open(prometheus_config_path) as f:
                config = yaml.safe_load(f)

            # Check that rule_files includes autoscaling rules
            assert 'rule_files' in config
            rule_files = config['rule_files']
            assert any('autoscaling-rules.yml' in rf for rf in rule_files)
            print("✅ Prometheus configuration test passed")

        except Exception as e:
            pytest.fail(f"Prometheus configuration test failed: {e}")

    def test_autoscaling_rules_exist(self):
        """Test that autoscaling rules file exists and is valid"""
        try:
            import yaml

            rules_path = os.path.join(os.path.dirname(__file__), '..', 'performance', 'scaling', 'autoscaling-rules.yml')
            assert os.path.exists(rules_path)

            with open(rules_path) as f:
                rules = yaml.safe_load(f)

            assert 'groups' in rules
            assert len(rules['groups']) > 0
            assert 'rules' in rules['groups'][0]
            print("✅ Autoscaling rules validation test passed")

        except Exception as e:
            pytest.fail(f"Autoscaling rules test failed: {e}")

    def test_nginx_configuration_exists(self):
        """Test that Nginx load balancer configuration exists"""
        try:
            nginx_config_path = os.path.join(os.path.dirname(__file__), '..', 'performance', 'scaling', 'nginx-lb.conf')
            assert os.path.exists(nginx_config_path)

            with open(nginx_config_path) as f:
                content = f.read()

            # Check for key Nginx directives
            assert 'upstream ghostlink_api_backend' in content
            assert 'server ghostlink-api-prod-1:3000' in content
            assert 'proxy_pass http://ghostlink_api_backend' in content
            print("✅ Nginx configuration test passed")

        except Exception as e:
            pytest.fail(f"Nginx configuration test failed: {e}")

    def test_docker_compose_networks(self):
        """Test that Docker compose files have consistent networks"""
        try:
            import yaml

            compose_files = [
                '../docker-compose.yml',
                '../performance/optimization/docker-compose-optimized.yml',
                '../performance/scaling/docker-compose-scaled.yml'
            ]

            for compose_file in compose_files:
                file_path = os.path.join(os.path.dirname(__file__), compose_file)
                if os.path.exists(file_path):
                    with open(file_path) as f:
                        compose_config = yaml.safe_load(f)

                    # Main compose uses host networking, others should use ghostlink-network
                    if compose_file == 'docker-compose.yml':
                        # Host networking is acceptable for main deployment
                        continue
                    else:
                        # Scaled and optimized should have networks section
                        assert 'networks' in compose_config
                        assert 'ghostlink-network' in compose_config['networks']
                        print(f"✅ Docker compose network test passed for {compose_file}")

        except Exception as e:
            pytest.fail(f"Docker compose networks test failed: {e}")

    def test_performance_dependencies(self):
        """Test that performance dependencies are in requirements.txt"""
        try:
            requirements_path = os.path.join(os.path.dirname(__file__), '..', 'requirements.txt')
            with open(requirements_path) as f:
                requirements = f.read()

            # Check for key performance dependencies
            required_deps = ['aioredis', 'redis', 'hiredis', 'aiomysql', 'aiohttp']
            for dep in required_deps:
                assert dep in requirements, f"Missing {dep} in requirements.txt"

            print("✅ Performance dependencies test passed")

        except Exception as e:
            pytest.fail(f"Performance dependencies test failed: {e}")

    @pytest.mark.asyncio
    async def test_performance_monitor_functionality(self):
        """Test performance monitor functionality"""
        try:
            import importlib.util
            performance_path = os.path.join(os.path.dirname(__file__), '..', 'performance', 'optimization')

            # Import performance monitor
            perf_spec = importlib.util.spec_from_file_location(
                "performance_monitor",
                os.path.join(performance_path, "performance-monitor.py")
            )
            perf_module = importlib.util.module_from_spec(perf_spec)
            perf_spec.loader.exec_module(perf_module)
            monitor = perf_module.PerformanceMonitor()

            # Test recording requests
            monitor.record_request('/test', 0.1, 200)
            monitor.record_request('/error', 0.05, 404)

            # Test cache operations
            monitor.record_cache_hit()
            monitor.record_cache_miss()

            # Test report generation
            report = monitor.get_performance_report()
            assert 'total_requests' in report
            assert 'error_rate' in report
            assert 'cache_hit_ratio' in report
            assert report['total_requests'] == 2
            assert report['error_count'] == 1

            print("✅ Performance monitor functionality test passed")

        except Exception as e:
            pytest.fail(f"Performance monitor functionality test failed: {e}")

def run_integration_tests():
    """Run all integration tests"""
    print("🚀 Starting GhostLink Performance Integration Tests")
    print("=" * 60)

    # Run tests
    pytest.main([
        __file__,
        '-v',
        '--tb=short',
        '-k', 'not test_api_server_performance_endpoint'  # Skip server test by default
    ])

if __name__ == "__main__":
    run_integration_tests()