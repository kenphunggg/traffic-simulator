"""
Interact with operting system
"""
import os
import csv
from time import time
from locust import (HttpUser,
                    task,
                    events
                    )
import numpy as np
from lib.log_csv import (LogLine, ReadCSV)
from lib.gen_data import GenerateData
from lib.anal_data import AnalyzeData as Analyze
########## CONFIG HERE ###########
# Take arguements



# Print Result
TEST_CASE = 'test_case'
RESULT_FILE = 'test'

RESULT_FILE_LOCATION = f'result_file/{TEST_CASE}/{RESULT_FILE}.csv'
INVOCATION_FILE_LOCATION = '../azure-sampleData/invocations/invocations_per_function_md.anon.d01.csv'
DURATION_FILE_LOCATION = '../azure-sampleData/function_durations/function_durations_percentiles.anon.d01.csv'
MEMORY_FILE_LOCATION = '../azure-sampleData/app_memory/app_memory_percentiles.anon.d01.csv'

# CONSTANTS
##### SET UP BASED ON DATATRACE #####

STEP_TIME = 8

######################################

class User(HttpUser):
    """Define User to execute Task"""
    host = 'http://localhost:28080/mem.php'
    
    def __init__(self, parent):
        super().__init__(parent)

        self.desire_row = 1              # Config this can change the app id and other information
        self.trigger_per_minute = 0
        self.execution_time = None
        self.memory_usage = None
        self.start_time = time()
        self.invocations_column = 4
        self.execution_time_data = []
        self.memory_usage_data = []
        self.app_id = None
        self.time_between_task = float(0)
        self.result_line_count = 1
    
    @task
    def user_behavior(self):
        """"
        Taskset for curl the http
        """
        # UPDATE TIME BETWEEN TASKS
        current_time = time()
        if self.result_line_count == 1:
            LogLine.header(RESULT_FILE_LOCATION)
        if self.invocations_column == 4 or current_time - self.start_time >= STEP_TIME:
            # Get App id
            self.app_id = ReadCSV.app_id(INVOCATION_FILE_LOCATION, self.desire_row)
            
            # Update time between task
            self.trigger_per_minute = ReadCSV.trigger_per_minute(INVOCATION_FILE_LOCATION,
                                                                 self.desire_row,
                                                                 self.invocations_column)
            self.time_between_task = ReadCSV.time_between_task(self.trigger_per_minute, STEP_TIME)
            
            self.start_time = current_time
            self.invocations_column += 1
        else:
            pass

        # UPDATE DURATION TIME
        if self.result_line_count == 1:
            self.execution_time_data = GenerateData.durations_data(self.app_id, DURATION_FILE_LOCATION)
        else:
            pass

        current_value = self.execution_time_data[0]
        self.execution_time_data = np.delete(self.execution_time_data, 0)
        self.execution_time = current_value
        
        # UPDATE RAM USAGE
        if self.result_line_count == 1:
            self.memory_usage_data = GenerateData.memory_data(self.app_id, MEMORY_FILE_LOCATION)
        else:
            pass

        current_value = self.memory_usage_data[0]
        self.memory_usage_data = np.delete(self.memory_usage_data, 0)
        self.memory_usage = current_value
        
        # SEND REQUEST
        response = self.client.request(
            method = 'GET',
            url = f'/?value={self.execution_time}&memory={self.memory_usage}'
        )
        
        # GET RESPONSE VALUE
        with open (f'{RESULT_FILE_LOCATION}', mode = 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                self.result_line_count,
                Analyze.get_response(response, "input_execution_time"),
                Analyze.get_response(response, "input_ram_usage"),
                Analyze.get_response(response, "response_time"),
                Analyze.get_response(response, "real_ram_usage"),
                Analyze.get_response(response, "formatted_time"),
                ])

        # Adjust line count for csv file
        self.result_line_count += 1
    
    def wait_time(self):
        """Define own wait time"""
        return self.time_between_task

class User2(User):
    """Define User to execute user_behavior"""
    def __init__(self, parent):
        super().__init__(parent)
        self.desire_row = 2


@events.init.add_listener
def on_init():
    """Execute on initiation"""
    os.system(f'touch {RESULT_FILE_LOCATION}')
    
