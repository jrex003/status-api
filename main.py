from fastapi import FastAPI, HTTPException
import psutil
import datetime

app = FastAPI()

@app.get("/uptime")
def get_uptime():
    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())

    return {
        "uptime": str(uptime),
    }

@app.get("/status")
def get_status():
    """Returns system status"""
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    if cpu_usage > 90 or memory_usage > 90 or disk_usage > 95:
        health_status = "unhealthy"
    elif cpu_usage > 70 or memory_usage > 75 or disk_usage > 80:
        health_status = "degraded"
    else:
        health_status = "healthy"
    return {
        "cpu_usage": f"{cpu_usage}%",
        "memory_usage": f"{memory_usage}%",
        "disk_usage": f"{disk_usage}%",
        "health_status": health_status
    }

@app.get("/top-processes")
def get_top_processes(limit: int = 10, sort_by: str = "cpu"):
    """
    Returns the top N processes sorted by either CPU or memory usage.
    Query Params:
    - limit (int): Number of processes to return (default: 10)
    - sort_by (str): Sorting criteria ("cpu" or "memory", default: "cpu")
    """

    if sort_by not in ["cpu", "memory"]:
        raise HTTPException(status_code=400, detail="sort_by must be either 'cpu' or 'memory'")
    
    if limit < 1:
        raise HTTPException(status_code=400, detail="limit must be greater than 0")

    process_list = [
        proc.info for proc in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_percent'])
        if proc.info['pid'] != 0  # Filter out PID 0 for System Idle Process
    ]

    if sort_by == "memory":
        process_list.sort(key=lambda x: x["memory_percent"], reverse=True)
    else:
        process_list.sort(key=lambda x: x["cpu_percent"], reverse=True)

    return {"top_processes": process_list[:limit]}