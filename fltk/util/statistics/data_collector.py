import logging
import os
from datetime import datetime


class DataCollector:
    _column_names = ['timestamp',
                     'num_nodes',
                     'current_utilisation',
                     'total_utilisation',
                     'estimated_nodes_num',
                     'pending_tasks_count']

    def __init__(self):
        self._output_file = None
        self._logger = logging.getLogger('DataCollector')
        self.initialize_file()
        self._header = ','.join(self._column_names)
        self._starting_time = datetime.now().timestamp()

    def initialize_file(self):
        self._logger.info("Spinning up data collection mechanism...")

        now = datetime.now().isoformat()
        file_name = f'{now}.csv'
        self._output_file = open(file_name, 'w')
        self._output_file.write(self._header + '\n')

    def log(self, num_nodes, current_utilisation, total_utilisation, estimated_nodes_num):
        timestamp = self._starting_time - datetime.now().timestamp()
        line = f'{timestamp},{num_nodes},{current_utilisation},{total_utilisation},{estimated_nodes_num}\n'
        self.write_line(line)

    def write_line(self, line):
        self._output_file.write(line)
        self._output_file.flush()
        os.fsync(self._output_file.fileno())

    def end_logging_session(self):
        self._output_file.close()
