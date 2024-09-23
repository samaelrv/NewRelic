import time
import requests
import schedule
import logging
from datetime import datetime
import newrelic.agent

# Initialize New Relic agent
newrelic.agent.initialize('newrelic.ini')

# Configure logging
logging.basicConfig(filename='status_log.log', level=logging.INFO)

# Global counter to keep track of task executions
execution_counter = 0

# Main function to simulate task and track metrics
@newrelic.agent.background_task()
def monitor_task():
    global execution_counter
    execution_counter += 1  # Increment the counter on each run

    start_time = time.time()  # Capture start time of the task
    try:
        if execution_counter % 3 == 0:
            # Simulate an exception every 3rd execution
            raise Exception("Simulated exception for testing purposes.")

        # Simulate a successful API call for other executions
        response = requests.get("https://jsonplaceholder.typicode.com/posts")
        response.raise_for_status()  # Raise exception if the request fails (status != 200)

        # Calculate execution time
        response_time = round(time.time() - start_time, 2)

        # Log success and send data to New Relic as a custom event
        logging.info(f"Task executed successfully at run {execution_counter}")
        newrelic.agent.record_custom_event("JobStatus", {
            "jobName": "BatchJob1",
            "status": "success",
            "responseTime": response_time,
            "runNumber": execution_counter,
            "timestamp": str(datetime.now())
        })

        # Print success status
        print(f"[{datetime.now()}] Run {execution_counter}: Task executed successfully. Response Time: {response_time} seconds.")

    except Exception as e:
        # Calculate response time even if the task fails
        response_time = round(time.time() - start_time, 2)

        # Log failure and send data to New Relic as a custom event
        logging.error(f"Task failed at run {execution_counter}: {e}")
        newrelic.agent.record_custom_event("JobStatus", {
            "status": "failure",
            "responseTime": response_time,
            "runNumber": execution_counter,
            "error": str(e),
            "timestamp": str(datetime.now())
        })

        # Print failure status
        print(f"[{datetime.now()}] Run {execution_counter}: Task failed with error: {e}. Response Time: {response_time} seconds.")

# Schedule the task to run every 5 minutes
schedule.every(1).minutes.do(monitor_task)

# Run the scheduled task
if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
