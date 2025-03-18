from fastapi import FastAPI, HTTPException
import psutil
import datetime
import time

app = FastAPI()

@app.get("/")
def root():
    return {
        "available_endpoints": {
            "GET /": "Directory",
            "GET /status": "System status and metrics",
            "GET /uptime": "System uptime information",
            "GET /top_processes": "Sorted list of top processes"
        },
    }

@app.get("/uptime")
def get_uptime():
    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())

    total_seconds = int(uptime.total_seconds())
    days = total_seconds // (24 * 3600)
    remaining = total_seconds % (24 * 3600)
    hours = remaining // 3600
    remaining = remaining % 3600
    minutes = remaining // 60
    seconds = remaining % 60

    uptime_parts = []

    if days > 0:
        uptime_parts.append(f"{days} {'day' if days == 1 else 'days'}")

    if hours > 0:
        uptime_parts.append(f"{hours} {'hour' if hours == 1 else 'hours'}")

    if minutes > 0:
        uptime_parts.append(f"{minutes} {'minute' if minutes == 1 else 'minutes'}")

    if seconds > 0 or not uptime_parts:
        uptime_parts.append(f"{seconds} {'second' if seconds == 1 else 'seconds'}")

    return {
        "uptime": ", ".join(uptime_parts),
        "components": {
            "days": days,
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds
        },
        "total_seconds": total_seconds
    }

@app.get("/status")
def get_status():
    """Returns system status and metrics"""
    cpu_usage = psutil.cpu_percent(interval=0.1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    if cpu_usage > 90 or memory_usage > 90 or disk_usage > 95:
        health_status = "unhealthy"
    elif cpu_usage > 70 or memory_usage > 75 or disk_usage > 80:
        health_status = "degraded"
    else:
        health_status = "healthy"
    
    return {
        "status": health_status,
        "metrics": {
            "cpu": {
                "usage_percent": cpu_usage
            },
            "memory": {
                "usage_percent": memory_usage
            },
            "disk": {
                "usage_percent": disk_usage
            }
        },
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

@app.get("/top_processes")
def get_top_processes(limit: int = 10, sort_by: str = "cpu", max_limit: int = 100):
    """
    Returns the top N processes sorted by either CPU or memory usage.
    Query Params:
    - limit (int): Number of processes to return (default: 10, max: 100)
    - sort_by (str): Sorting criteria ("cpu" or "memory", default: "cpu")
    """
    if sort_by not in ["cpu", "memory"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort parameter: sort_by must be either 'cpu' or 'memory'"
        )

    if limit < 1 or limit > max_limit:
        raise HTTPException(
            status_code=400, 
            detail=f"limit must be between 1 and {max_limit}"
        )

    # Initial call to avoid getting 0% CPU usage
    for proc in psutil.process_iter(['cpu_percent']):
        pass
    
    time.sleep(0.1)
    
    process_list = [
        proc.info for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent'])
        if proc.info['pid'] != 0  # Filter out PID 0 for System Idle Process
    ]

    if sort_by == "memory":
        process_list.sort(key=lambda x: x["memory_percent"], reverse=True)
    else:
        process_list.sort(key=lambda x: x["cpu_percent"], reverse=True)

    return {
        "data": {
            "processes": process_list[:limit]
        },
        "metadata": {
            "total_processes": len(process_list),
            "returned_processes": min(limit, len(process_list)),
            "sorted_by": sort_by,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
    }