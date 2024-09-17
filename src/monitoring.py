import asyncio
import time
from logger import setup_logger
import psutil

monitor_logger = setup_logger('monitor', 'logs/monitor.log')

class ServiceMonitor:
    def __init__(self, services):
        self.services = services
        self.service_status = {service: "Unknown" for service in services}

    async def check_service(self, service):
        try:
            # Here we'll implement a simple health check
            # In a real-world scenario, you'd want to implement more robust checks
            result = await service.arun({"query": "Health check"})
            if result:
                self.service_status[service] = "Healthy"
            else:
                self.service_status[service] = "Unhealthy"
        except Exception as e:
            self.service_status[service] = f"Error: {str(e)}"

    async def monitor_services(self):
        while True:
            tasks = [self.check_service(service) for service in self.services]
            await asyncio.gather(*tasks)
            self.log_status()
            await asyncio.sleep(60)  # Check every 60 seconds

    def log_status(self):
        for service, status in self.service_status.items():
            monitor_logger.info(f"Service {service.__name__}: {status}")

class SystemMonitor:
    def __init__(self):
        self.start_time = time.time()
        monitor_logger.info("SystemMonitor initialized")

    def get_system_metrics(self):
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')

            metrics = {
                'cpu_usage': cpu_percent,
                'memory_usage': memory.percent,
                'disk_usage': disk.percent
            }

            monitor_logger.info(f"Collected metrics: {metrics}")
            return metrics
        except Exception as e:
            monitor_logger.error(f"Error collecting system metrics: {str(e)}")
            return {'error': f'Failed to collect system metrics: {str(e)}'}

async def run_monitor(services):
    monitor = ServiceMonitor(services)
    await monitor.monitor_services()

# This can be called from workflows.py after deploying the services
# asyncio.create_task(run_monitor([information_service_deployed, calculation_service_deployed, summarization_service_deployed, action_service_deployed]))