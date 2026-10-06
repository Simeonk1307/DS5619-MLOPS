This is a tiny Python tool built for our week 9 class session. It mimics how Airflow schedules pipelines and retries tasks, but runs completely locally in a single file so we don't have to spin up heavy databases or web servers.
What it does:

* Figure outs the right order to run tasks based on their dependencies so things don't crash.
* Retries individual tasks if they hit a temporary error, waiting a few seconds between tries.
* Passes a shared dictionary along so downstream tasks can use data from earlier steps.
* Stops the pipeline immediately if a task runs out of retries, making sure broken data doesn't move forward.

Files included:

* orchestrator.py: Holds the code for the scheduler, retries, and runner.
* NOTES.md: My answers about how the tasks run and the FinOps cost of retrying APIs.
