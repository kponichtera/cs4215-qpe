import abc
from typing import List


class Estimator:

    @abc.abstractmethod
    def estimate_arrival_rate(self) -> float:
        raise NotImplementedError()


class ArrivalRateEstimator(Estimator):
    job_counter: int = 0
    job_execution_times: List[float]

    def __init__(self):
        super().__init__()
        pass

    def new_arrival(self):
        self.job_counter += 1

    def new_job_finish(self, job_execution_time):
        self.job_execution_times.append(job_execution_time)

    def estimate_arrival_rate(self) -> float:
        return 2.5
