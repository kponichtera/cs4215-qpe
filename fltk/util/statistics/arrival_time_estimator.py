from typing import List


class ArrivalTimeEstimator:
    job_counter: int = 0
    job_execution_times: List[float]

    def __init__(self):
        pass

    def new_arrival(self):
        self.job_counter += 1

    def new_job_finish(self, job_execution_time):
        self.job_execution_times.append(job_execution_time)