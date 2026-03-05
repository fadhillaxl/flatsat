import time
import threading

class Scheduler:
    def __init__(self):
        self.tasks = []
        self.running = False
        self.thread = None

    def add_task(self, interval, func):
        self.tasks.append({"interval": interval, "func": func, "last_run": 0})

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()
        print("[Scheduler] Started.")

    def _run(self):
        while self.running:
            now = time.time()
            for task in self.tasks:
                if now - task["last_run"] >= task["interval"]:
                    try:
                        print(f"[Scheduler] Running task: {task['func'].__name__}")
                        task["func"]()
                    except Exception as e:
                        print(f"[Scheduler] Task failed: {e}")
                    task["last_run"] = now
            time.sleep(1)

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        print("[Scheduler] Stopped.")
