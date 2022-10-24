import abc
from datetime import datetime
from typing import List, Optional


class Estimator:

    @abc.abstractmethod
    def estimate_arrival_rate(self) -> Optional[float]:
        raise NotImplementedError()

    @abc.abstractmethod
    def estimate_service_rate(self) -> Optional[float]:
        raise NotImplementedError()

    @abc.abstractmethod
    def reset(self):
        raise NotImplementedError()


class ArrivalRateEstimator(Estimator):

    inter_arrival_counter = 0
    completed_jobs_counter = 0
    service_time_sum = 0
    inter_arrival_sum = 0
    previous_arrival_timestamp = None

    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        self.inter_arrival_counter = 0
        self.completed_jobs_counter = 0
        self.service_time_sum = 0
        self.inter_arrival_sum = 0
        self.previous_arrival_timestamp = None

    def new_arrival(self):
        new_timestamp = datetime.now()
        if self.previous_arrival_timestamp is not None:
            self.inter_arrival_counter += 1
            inter_arrival_time = new_timestamp - self.previous_arrival_timestamp
            self.inter_arrival_sum += inter_arrival_time.total_seconds()
        self.previous_arrival_timestamp = new_timestamp

    def new_job_finish(self, job_execution_time):
        self.completed_jobs_counter += 1
        self.service_time_sum += job_execution_time

    def estimate_arrival_rate(self) -> Optional[float]:
        if self.inter_arrival_counter != 0:
            mean_inter_arrival_time = self.inter_arrival_sum / self.inter_arrival_counter
            return 1 / mean_inter_arrival_time
        else:
            return None

    def estimate_service_rate(self) -> Optional[float]:
        if self.completed_jobs_counter != 0:
            mean_service_time = self.service_time_sum / self.completed_jobs_counter
            return 1 / mean_service_time
        else:
            return None
