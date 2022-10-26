import os
from datetime import datetime


class DataCollector:
    output_file = None

    def __init__(self):
        self.initialize_file()

    def initialize_file(self):
        now = datetime.now()
        file_name = f'{now.strftime("%Y/%m/%d %H:%M:%S")}.log'
        self.output_file = open(file_name, 'w')
        self.output_file.write('timestamp,num_nodes,current_utilisation,total_utilisation,estimated_nodes_num\n')

    def log(self, num_nodes, current_utilisation, total_utilisation, estimated_nodes_num):
        now = datetime.now().strftime("%H:%m:%S")
        line = f'{now},{num_nodes},{current_utilisation},{total_utilisation},{estimated_nodes_num}\n'
        self.write_line(line)

    def write_line(self, line):
        self.output_file.write(line)
        self.output_file.flush()
        os.fsync(self.output_file.fileno())

    def end_logging_session(self):
        self.output_file.close()
