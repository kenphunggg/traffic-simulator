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
from lib.log_csv import (LogLine, 
                         GetData,
                         AnalyzeData as Analyze)
from lib.gen_data import GenerateData
# from lib.analyze_data import AnalyzeData as Analyze

########## RESULT CONFIG ##############

TEST_CASE = 'test_case'
RESULT_FILE = 'test'

############ FILE LOCATION #############

RESULT_FILE_LOCATION = f'result_file/{TEST_CASE}/{RESULT_FILE}.csv'
INVOCATION_FILE_LOCATION = '../azure-sampleData/invocations/invocations_per_function_md.anon.d01.csv'
DURATION_FILE_LOCATION = '../azure-sampleData/function_durations/function_durations_percentiles.anon.d01.csv'
MEMORY_FILE_LOCATION = '../azure-sampleData/app_memory/app_memory_percentiles.anon.d01.csv'

###### SET UP BASED ON DATATRACE ######

STEP_TIME = 60

########################################

class User1(HttpUser):
    """Define User to execute Task"""
    result_line_count = 1  # It can only change by first user cuz i do not know how to do it another way
    init = 1
    host = 'http://localhost:28001/mem.php'

    def __init__(self, parent):
        super().__init__(parent)
        
        self.app_id = None
        self.init = 1
        self.desire_app_count = 1
        
        # For Invocations file
        self.start_time = time()
        self.trigger_per_minute = 0
        self.time_between_task = float(0)
        self.invocations_column = 4
        # For Execution time
        self.execution_time = None
        self.execution_time_data = []
        # For Memory usage
        self.memory_usage = None
        self.memory_usage_data = []

    @task
    def user_behavior(self):
        """"
        Taskset for curl the http
        """
        # UPDATE TIME BETWEEN TASKS
        if User1.init == 1:
            LogLine.header(RESULT_FILE_LOCATION)
            User1.init -= 1
        # GENERATE INITIAL DATA
        if self.init == 1:
            self.app_id = GetData.app_id(desire_app_count=self.desire_app_count,
                                         file=INVOCATION_FILE_LOCATION)
            self.execution_time_data = GenerateData.durations_data(self.app_id, DURATION_FILE_LOCATION)
            self.memory_usage_data = GenerateData.memory_data(self.app_id, MEMORY_FILE_LOCATION)
            self.init -= 1
        
        if self.trigger_per_minute != 0:
            
            # UPDATE DURATION TIME
            self.execution_time = self.execution_time_data[0]
            self.execution_time_data = np.delete(self.execution_time_data, 0)
                
            # UPDATE RAM USAGE
            self.memory_usage = self.memory_usage_data[0]
            self.memory_usage_data = np.delete(self.memory_usage_data, 0)
            
            # SEND REQUEST
            response = self.client.request(
                method='POST',
                url='',
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                data={
                    'value': self.execution_time,
                    'memory': self.memory_usage
                }
            )
            
            # GET RESPONSE VALUE
            with open (f'{RESULT_FILE_LOCATION}', mode = 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    User1.result_line_count,
                    Analyze.get_response(response, "input_execution_time"),
                    Analyze.get_response(response, "input_ram_usage"),
                    Analyze.get_response(response, "response_time"),
                    Analyze.get_response(response, "real_ram_usage"),
                    Analyze.get_response(response, "formatted_time"),
                    self.app_id
                    ])

            # Adjust line count for csv file
            User1.result_line_count += 1

    def wait_time(self):
        """Define own wait time"""
        current_time = time()
        if self.invocations_column == 4 or current_time - self.start_time >= STEP_TIME:
            # Update time between task
            self.app_id = GetData.app_id(desire_app_count=self.desire_app_count,
                                         file=INVOCATION_FILE_LOCATION)
            
            self.trigger_per_minute = GetData.trigger_per_minute(app_id=self.app_id,
                                                                 column=self.invocations_column,
                                                                 file=INVOCATION_FILE_LOCATION)
            
            self.time_between_task = GetData.time_between_task(self.trigger_per_minute, STEP_TIME)
            
            self.start_time = current_time
            self.invocations_column += 1
        return self.time_between_task


@events.init.add_listener
def on_init():
    """Execute on initiation"""
    os.system(f'touch {RESULT_FILE_LOCATION}')

class User2(User1):
    """Define User to execute user_behavior"""
    host = 'http://localhost:28002/mem.php'
    def __init__(self, parent):
        super().__init__(parent)
        self.desire_app_count = 2
    