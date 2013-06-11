#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import threading
import time
import Queue

class Manager:

    """
    @args：
        max_works_count :
    @desc:
    """

    def __init__(self, max_worker_count=5):
        self.tasks = Queue.Queue()
        self.max_worker_count = max_worker_count

    def put_task(self, task):
        self.tasks.put(task)

    def put_tasks(self, tasks):
        for task in tasks:
            self.put_task(task)

    def get_task(self):
        self.tasks.get()

    def do_task(self):
        while 1:
            sub_task = self.tasks.get()
            if sub_task:
                sub_task.run()

    def _task_run(self):
        for _ in range(self.max_worker_count):
            worker = threading.Thread(target=self.do_task)
            worker.start()
        time.sleep(2)

    def run(self):

        master = threading.Thread(target=self._task_run)
        master.daemon = True
        master.start()
        
        
class Task:

    def __init__(self, name="Base Task"):
        self.name = name

    def do_task(self):
        raise NotImplementedError("Not implemention")

    def run(self):
        raise NotImplementedError("Not implemention")
