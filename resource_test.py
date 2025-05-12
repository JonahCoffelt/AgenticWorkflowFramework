import psutil
import os
import time

def get_resource_usage():
    process = psutil.Process(os.getpid())
    cpu_usage = process.cpu_percent(interval=1)
    memory_usage = process.memory_info().rss / 1024 ** 2  # in MB
    return cpu_usage, memory_usage

if __name__ == "__main__":
    # Your Python code here
    # Example:
    t = 1
    for i in range(100000):
        t *= i 

    cpu_percent, mem_mb = get_resource_usage()
    print(f"CPU Usage: {cpu_percent}%")
    print(f"Memory Usage: {mem_mb:.2f} MB")
