# Status API

Access information on the status and health of your system. Data will be returned in JSON format.

## Installation
1. Clone the repository
```bash
git https://github.com/jrex003/status-api.git
```
2. Navigate to the project directory after cloning
```bash
cd status-api
```
3. Activate the virtual environment
```bash
.\venv\Scripts\activate
```
4. Install the dependencies
```bash
pip install -r requirements.txt
```
## How to use the API

Start the server by typing the following command in the terminal. You will then be able to access the API at `http://127.0.0.1:8000`
```
uvicorn main:app --reload
```
## Endpoints
Type in the desired endpoint after the base URL
```
http://127.0.0.1:8000/{endpoint}
```

If parameters are needed, type them after the endpoint in the format `?param1=value1&param2=value2`
```
http://127.0.0.1:8000/{endpoint}?param1=value1&param2=value2
```

### GET /uptime
This endpoint returns the uptime of your system.
```json
{
  "uptime": "4 days, 13 hours, 39 minutes, 20 seconds",
  "components": {
    "days": 4,
    "hours": 13,
    "minutes": 39,
    "seconds": 20
  },
  "total_seconds": 394760
}
```

### GET /status
This endpoint returns the status and metrics of your system.
The status is defined as follows:
- healthy: if cpu_usage < 70%, memory_usage < 75%, and disk_usage < 80%
- degraded: if cpu_usage > 70%, memory_usage > 75%, and disk_usage > 80%
- unhealthy: if cpu_usage > 90%, memory_usage > 90%, and disk_usage > 95%
```json
{
  "status": "healthy",
  "metrics": {
    "cpu": {
      "usage_percent": 26.5
    },
    "memory": {
      "usage_percent": 68.6
    },
    "disk": {
      "usage_percent": 66.9
    }
  },
  "timestamp": "2025-03-18T01:32:16.451690+00:00"
}
```

### GET /top_processes
This endpoint returns the top N processes sorted by either CPU or memory usage.
Parameters:
- limit: Number of processes to return (default: 10, max: 100)
- sort_by: Sorting criteria ("cpu" or "memory", default: "cpu")

If no parameters are provided, the default values will be used.
```json
{
  "data": {
    "processes": [
      {
        "memory_percent": 4.00213180155188,
        "pid": 16244,
        "name": "chrome.exe",
        "cpu_percent": 2.9
      },
      {
        "memory_percent": 3.32935974845508,
        "pid": 4880,
        "name": "Corsair.Service.exe",
        "cpu_percent": 5.7
      },
      {
        "memory_percent": 2.01465302320058,
        "pid": 35656,
        "name": "RiotClientServices.exe",
        "cpu_percent": 0
      },
      {
        "memory_percent": 1.92381682499954,
        "pid": 6024,
        "name": "steamwebhelper.exe",
        "cpu_percent": 0
      },
      {
        "memory_percent": 1.72394845847811,
        "pid": 2904,
        "name": "MemCompression",
        "cpu_percent": 0
      },
      {
        "memory_percent": 1.64968016991205,
        "pid": 18020,
        "name": "Discord.exe",
        "cpu_percent": 0
      },
      {
        "memory_percent": 1.62578598809744,
        "pid": 2148,
        "name": "MsMpEng.exe",
        "cpu_percent": 0
      },
    ]
  },
  "metadata": {
    "total_processes": 368,
    "returned_processes": 7,
    "sorted_by": "memory",
    "timestamp": "2025-03-18T18:01:48.573262+00:00"
  }
}
```