import abc
from datetime import datetime
from typing import List, Optional


class Estimator:

    @abc.abstractmethod
    def estimate_utilization(self, current_node_count: int) -> Optional[float]:
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


class ArrivalRateEstimator(Estimator):
    previous_arrival_timestamp = None
    last_3_inter_arrival_times = []

    def __init__(self):
        super().__init__()
        self.total_completed_jobs_counter = 0
        self.total_response_time_sum = 0

    def new_arrival(self):
        new_timestamp = datetime.now()
        if self.previous_arrival_timestamp is not None:
            inter_arrival_time = new_timestamp - self.previous_arrival_timestamp
            if len(self.last_3_inter_arrival_times) >= 3:
                self.last_3_inter_arrival_times.pop(0)
            self.last_3_inter_arrival_times.append(inter_arrival_time.total_seconds())
        self.previous_arrival_timestamp = new_timestamp

    def new_job_finish(self, job_service_time, job_response_time):
        self.total_completed_jobs_counter += 1
        self.total_response_time_sum += job_response_time

    def estimate_utilization(self, current_node_count: int) -> Optional[float]:
        service_rate = self.estimate_service_rate()
        arrival_rate = self.estimate_arrival_rate()
        if service_rate is None or arrival_rate is None:
            return None
        service_rate *= current_node_count

        return arrival_rate / service_rate

    def estimate_response_time(self) -> Optional[float]:
        if self.total_completed_jobs_counter == 0:
            return None
        return self.total_response_time_sum / self.total_completed_jobs_counter

    def estimate_service_rate(self) -> Optional[float]:
        return self._estimate_service_rate()

    def estimate_arrival_rate(self) -> Optional[float]:
        return self._estimate_arrival_rate(self.last_3_inter_arrival_times)

    def _estimate_arrival_rate(self, inter_arrival_rates) -> Optional[float]:
        if len(inter_arrival_rates) != 0:
            return 1 / (sum(inter_arrival_rates) / len(inter_arrival_rates))
        else:
            return None

    def _estimate_service_rate(self) -> Optional[float]:
        return 1/105
