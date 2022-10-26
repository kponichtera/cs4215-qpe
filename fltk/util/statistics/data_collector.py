import logging
import os
import time
from datetime import datetime


class DataCollector:
    _column_names = ['time',
                     'num_nodes',
                     'estimated_nodes_num',
                     'current_utilisation',
                     'total_utilisation',
                     'total_average_response_time',
                     'pending_tasks_count']

    def __init__(self):
        self._output_file = None
        self._start_time = None
        self._logger = logging.getLogger('DataCollector')
        self._header = ','.join(self._column_names)
        self.initialize_file()

    def initialize_file(self):
        self._logger.info("Spinning up data collection mechanism...")
        now = int(time.time())
        file_name = f'orchestrator_results_{now}.csv'
        self._output_file = open(file_name, 'w')
        self._output_file.write(self._header + '\n')

    def log(self, num_nodes, estimated_nodes_num, current_utilisation, total_utilisation, total_average_response_time, pending_tasks_count):
        if self._start_time is None:
            self._start_time = time.time()
            now = self._start_time
        else:
            now = time.time()

        time_since_start = now - self._start_time

        line = f'{time_since_start},{num_nodes},{estimated_nodes_num},{current_utilisation},{total_utilisation},{total_average_response_time},{pending_tasks_count}\n'
        self.write_line(line)

    def write_line(self, line):
        self._output_file.write(line)
        self._output_file.flush()
        os.fsync(self._output_file.fileno())

    def end_logging_session(self):
        self._logger.info("Closing the data output file...")
        self._output_file.close()
