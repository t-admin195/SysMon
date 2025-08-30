import psutil
import time
import subprocess

def get_cpu_metrics():
    return psutil.cpu_percent(interval=1)
def get_ram_metrics():
    return psutil.virtual_memory().percent
def get_logs():
    result = subprocess.run(["journalctl", "-n", "5"], capture_output=True, text=True)
    return result.stdout
def get_uptime():
    result = subprocess.run(["uptime"], capture_output=True, text=True)
    return result.stdout

while True:
    print(f"CPU: {get_cpu_metrics()}")
    print(f"RAM: {get_ram_metrics()}")
    print(f"LOGS:\n{get_logs()}")
    print(f"UPTIME:{get_uptime()}")
    time.sleep(5)
if __name__ == "__main__":
    main()