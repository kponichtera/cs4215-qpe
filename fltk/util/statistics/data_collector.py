import logging
import os
from datetime import datetime


class DataCollector:

    def __init__(self):
        self._output_file = None
        self._logger = logging.getLogger('DataCollector')
        self.initialize_file()

    def initialize_file(self):
        self._logger.info("Spinning up data collection mechanism...")
        now = datetime.now().isoformat()
        file_name = f'{now}.log'
        self._output_file = open(file_name, 'w')
        self._output_file.write('timestamp,num_nodes,current_utilisation,total_utilisation,estimated_nodes_num\n')

    def log(self, num_nodes, current_utilisation, total_utilisation, estimated_nodes_num):
        now = datetime.now().strftime("%H:%m:%S")
        line = f'{now},{num_nodes},{current_utilisation},{total_utilisation},{estimated_nodes_num}\n'
        self.write_line(line)

    def write_line(self, line):
        self._output_file.write(line)
        self._output_file.flush()
        os.fsync(self._output_file.fileno())

    def end_logging_session(self):
        self._output_file.close()
