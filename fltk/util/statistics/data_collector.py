import logging
import os
import time
from multiprocessing.pool import ThreadPool

from fltk.util.scaling.scaler import ClusterScaler
from fltk.util.statistics.arrival_rate_estimator import ArrivalRateEstimator


class DataCollector:
    SLEEP_TIME = 5

    _column_names = ['time',
                     'num_nodes',
                     'estimated_nodes_num',
                     'utilisation',
                     'arrival_rate',
                     'service_rate',
                     'total_average_response_time']

    def __init__(self, cluster_scaler: ClusterScaler, arrival_rate_estimator: ArrivalRateEstimator, ):
        self._alive = False
        self._thread_pool = ThreadPool(processes=1)
        self._logger = logging.getLogger('DataCollector')
        self._cluster_scaler = cluster_scaler
        self._arrival_rate_estimator = arrival_rate_estimator

        self._output_file = None
        self._start_time = None
        self._header = ','.join(self._column_names)

    def start(self):
        self._logger.info("Starting data collector...")
        self._alive = True
        self._thread_pool.apply_async(self._run)

    def stop(self):
        self._logger.info("Stopping data collector...")
        self._alive = False

    def _run(self):
        self._initialize_file()
        while self._alive:
            self._collect_data()
            time.sleep(self.SLEEP_TIME)
        self._end_logging_session()
        self._logger.info("Successfully stopped data collector")

    def _collect_data(self):
        self._logger.info("Logging state to the file...")
        current_node_count = self._cluster_scaler.determine_current_node_count()

        self._log(
            num_nodes=current_node_count,
            estimated_nodes_num=self._cluster_scaler.determine_requested_node_count(current_node_count),
            utilisation=self._arrival_rate_estimator.estimate_utilization(current_node_count),
            arrival_rate=self._arrival_rate_estimator.estimate_arrival_rate(),
            service_rate=self._arrival_rate_estimator.estimate_service_rate() * current_node_count,
            total_average_response_time=self._arrival_rate_estimator.estimate_response_time())

    def _initialize_file(self):
        now = int(time.time())
        file_name = f'orchestrator_results_{now}.csv'
        self._logger.info(f"Creating results file {file_name}")
        self._output_file = open(file_name, 'w')
        self._output_file.write(self._header + '\n')

    def _log(self, num_nodes, estimated_nodes_num, utilisation, arrival_rate, service_rate,
             total_average_response_time):
        if self._start_time is None:
            self._start_time = time.time()
            now = self._start_time
        else:
            now = time.time()

        time_since_start = now - self._start_time

        line = f'{time_since_start},{num_nodes},{estimated_nodes_num},{utilisation},{arrival_rate},{service_rate},{total_average_response_time}\n'
        self._write_line(line)

    def _write_line(self, line):
        self._output_file.write(line)
        self._output_file.flush()
        os.fsync(self._output_file.fileno())

    def _end_logging_session(self):
        self._logger.info("Closing the data output file...")
        self._output_file.close()
