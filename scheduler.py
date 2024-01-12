import schedule as s
import threading


class Task:
    def __init__(self, task, *args, **kwargs):
        self.task = task
        self.args = args
        self.kwargs = kwargs
        self._job = None
        self._on_done = None

    def do(self):
        _return = self.task(*self.args, **self.kwargs)
        self._job = None
        if self._on_done is not None:
            threading.Thread(target=self._on_done, args=[_return]).start()
        return s.CancelJob

    def on_done(self, func):
        self._on_done = func

    def at(self, time: str):
        self._job = s.every().day.at(time).do(self.do)
        return self

    def cancel(self):
        if self._job is not None:
            s.cancel_job(self._job)


class DailyTask:
    def __init__(self, task, *args, **kwargs):
        self.task = task
        self.args = args
        self.kwargs = kwargs
        self._job = None
        self._on_done = None
        self._return = None

    def do(self):
        _return = self.task(*self.args, **self.kwargs)
        if self._on_done is not None:
            self._on_done(_return)

    def on_done(self, func):
        self._on_done = func

    def at(self, time: str):
        self._job = s.every().day.at(time).do(self.do)
        return self

    def cancel(self):
        if self._job is not None:
            s.cancel_job(self._job)


def schedule(task, *args, **kwargs):
    return Task(task, *args, **kwargs)


def schedule_daily(task, *args, **kwargs):
    return DailyTask(task, *args, **kwargs)
