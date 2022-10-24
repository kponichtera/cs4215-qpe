import abc
from datetime import datetime
from typing import List


class Estimator:

    @abc.abstractmethod
    def estimate_arrival_rate(self) -> float:
        raise NotImplementedError()


class ArrivalRateEstimator(Estimator):
    job_counter: int = 0
    job_execution_times: List[float] = list()
    previous_arrival_timestamp = None
    inter_arrival_sum = 0

    def __init__(self):
        super().__init__()
        pass

    def new_arrival(self):
        new_timestamp = datetime.now()
        if self.previous_arrival_timestamp is not None:
            self.job_counter += 1
            inter_arrival_time = new_timestamp - self.previous_arrival_timestamp
            self.inter_arrival_sum += inter_arrival_time.total_seconds()
        self.previous_arrival_timestamp = new_timestamp

    def new_job_finish(self, job_execution_time):
        self.job_execution_times.append(job_execution_time)

    def estimate_arrival_rate(self) -> float:
        if self.job_counter != 0:
            mean_inter_arrival_time = self.inter_arrival_sum / self.job_counter
            return 1 / mean_inter_arrival_time
        else:
            return None
