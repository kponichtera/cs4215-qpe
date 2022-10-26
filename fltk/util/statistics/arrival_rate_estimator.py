import abc
from datetime import datetime
from typing import List, Optional


class Estimator:

    @abc.abstractmethod
    def estimate_utilization(self) -> Optional[float]:
        raise NotImplementedError()

    @abc.abstractmethod
    def estimate_arrival_rate(self) -> Optional[float]:
        raise NotImplementedError()

    @abc.abstractmethod
    def estimate_service_rate(self) -> Optional[float]:
        raise NotImplementedError()

    @abc.abstractmethod
    def estimate_response_time(self) -> Optional[float]:
        raise NotImplementedError()

    @abc.abstractmethod
    def reset(self):
        raise NotImplementedError()


class ArrivalRateEstimator(Estimator):

    total_inter_arrival_counter = 0
    total_completed_jobs_counter = 0
    total_service_time_sum = 0
    total_inter_arrival_sum = 0

    inter_arrival_counter = 0
    completed_jobs_counter = 0
    service_time_sum = 0
    inter_arrival_sum = 0

    previous_arrival_timestamp = None

    def __init__(self):
        super().__init__()
        self.total_inter_arrival_counter = 0
        self.total_completed_jobs_counter = 0
        self.total_service_time_sum = 0
        self.total_inter_arrival_sum = 0
        self.total_response_time_sum = 0
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
            self.total_inter_arrival_counter += 1
            inter_arrival_time = new_timestamp - self.previous_arrival_timestamp
            self.inter_arrival_sum += inter_arrival_time.total_seconds()
            self.total_inter_arrival_sum += inter_arrival_time.total_seconds()
        self.previous_arrival_timestamp = new_timestamp

    def new_job_finish(self, job_service_time, job_response_time):
        self.completed_jobs_counter += 1
        self.total_completed_jobs_counter += 1
        self.service_time_sum += job_service_time
        self.total_service_time_sum += job_service_time
        self.total_response_time_sum += job_response_time

    def estimate_utilization(self) -> Optional[float]:
        service_rate = self.estimate_service_rate()
        arrival_rate = self.estimate_arrival_rate()
        if service_rate is None or arrival_rate is None:
            return None

        return arrival_rate / service_rate

    def estimate_total_utilization(self) -> Optional[float]:
        service_rate = self.estimate_total_service_rate()
        arrival_rate = self.estimate_total_arrival_rate()
        if service_rate is None or arrival_rate is None:
            return None

        return arrival_rate / service_rate

    def estimate_response_time(self) -> Optional[float]:
        if self.total_completed_jobs_counter == 0:
            return None
        return self.total_response_time_sum / self.total_completed_jobs_counter

    def estimate_service_rate(self) -> Optional[float]:
        return self._estimate_service_rate(self.completed_jobs_counter, self.service_time_sum)

    def estimate_arrival_rate(self) -> Optional[float]:
        return self._estimate_arrival_rate(self.inter_arrival_counter, self.inter_arrival_sum)

    def estimate_total_arrival_rate(self) -> Optional[float]:
        return self._estimate_arrival_rate(self.total_inter_arrival_counter, self.total_inter_arrival_sum)

    def estimate_total_service_rate(self) -> Optional[float]:
        return self._estimate_service_rate(self.total_completed_jobs_counter, self.total_service_time_sum)

    def _estimate_arrival_rate(self, inter_arrival_counter, inter_arrival_sum) -> Optional[float]:
        if inter_arrival_counter != 0:
            mean_inter_arrival_time = inter_arrival_sum / inter_arrival_counter
            return 1 / mean_inter_arrival_time
        else:
            return None

    def _estimate_service_rate(self, completed_jobs_counter, service_time_sum) -> Optional[float]:
        if completed_jobs_counter != 0:
            mean_service_time = service_time_sum / completed_jobs_counter
            return 1 / mean_service_time
        else:
            return None
