import time
import psutil
from .monitor import check_site
from concurrent.futures import ThreadPoolExecutor

# Monothreading
def monothreading_verification(sites):
    start_time = time.time()
    for site in sites:
        url, status, duration = check_site(site)
        print(f"{url:<30} | {status:<6} | {duration} ms")
    end_time = time.time()
    return end_time - start_time

# Multithreading
def multithreading_verification(sites):
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=len(sites)) as executor:
        results = executor.map(check_site, sites)
        for url, status, duration in results:
            print(f"{url:<30} | {status:<6} | {duration} ms")
    end_time = time.time()
    return end_time - start_time

# Monitoramento com controle por evento e container externo
def monitor_system_usage(stop_event, data_container):
    cpu_usage = []
    memory_usage = []
    while not stop_event.is_set():
        cpu_usage.append(psutil.cpu_percent(interval=0.1))
        memory_usage.append(psutil.virtual_memory().percent)
    data_container["cpu"] = cpu_usage
    data_container["memory"] = memory_usage
