"""
Interact with operting system
"""
import os
import csv
from time import time, localtime, strftime
from locust import (HttpUser,
                    SequentialTaskSet,
                    task,
                    events
                    )
import numpy as np
from lib.log_csv import (LogLine, ReadCSV)
from lib.gen_data import GenerateData

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

class AdvanceCurlTask(SequentialTaskSet):
    """Setting tasks for user"""
    time_between_task = float(0)
    RESULT_LINE_COUNT = 1
    def __init__(self, parent):
        super().__init__(parent)
        self.trigger_per_minute = 0
        self.execution_time = None
        self.memory_usage = None
        self.start_time = time()
        self.invocations_column = 4
        
        
        self.execution_time_data = []
        self.memory_usage_data = []
        self.app_id = None
        self.desire_row = 1

    @task
    def update_time_between_task(self):
        """Update time between tasks based on number of trigger per minute"""
        # On Init
        if AdvanceCurlTask.RESULT_LINE_COUNT == 1:
            LogLine.header(RESULT_FILE_LOCATION)
        
        current_time = time()
        
        if self.invocations_column == 4 or current_time - self.start_time >= STEP_TIME:
            # Get App id
            self.app_id = ReadCSV.app_id(INVOCATION_FILE_LOCATION, self.desire_row)
            LogLine.get_app_id(self.app_id, RESULT_FILE_LOCATION)
            
            # Update time between task
            self.trigger_per_minute = ReadCSV.trigger_per_minute(INVOCATION_FILE_LOCATION,
                                                                 self.desire_row,
                                                                 self.invocations_column)
            AdvanceCurlTask.time_between_task = ReadCSV.time_between_task(self.trigger_per_minute, STEP_TIME)
            
            LogLine.invocations_update(self.trigger_per_minute,
                                       self.time_between_task, 
                                       self.invocations_column,
                                       RESULT_FILE_LOCATION)
            
            self.start_time = current_time
            self.invocations_column += 1
        else:
            LogLine.invocations_not_update(self.trigger_per_minute,
                                           self.time_between_task,
                                           self.invocations_column,
                                           RESULT_FILE_LOCATION)
            

    @task
    def update_execution_time(self):
        """Update execution time to insert to URL"""
        self.execution_time = 5
        if AdvanceCurlTask.RESULT_LINE_COUNT == 1:
            self.execution_time_data = GenerateData.durations_data(self.app_id, DURATION_FILE_LOCATION)
        else:
            pass
        # LogLine.update_status(type(data), RESULT_FILE_LOCATION)
        current_value = self.execution_time_data[0]
        self.execution_time_data = np.delete(self.execution_time_data, 0)
        
        self.execution_time = current_value
        LogLine.update_status('execution time', RESULT_FILE_LOCATION)
        
  
    @task
    def update_memory_usage(self):
        """Update RAM usage to insert to URL"""
        self.memory_usage = 10
        if AdvanceCurlTask.RESULT_LINE_COUNT == 1:
            self.memory_usage_data = GenerateData.memory_data(self.app_id, MEMORY_FILE_LOCATION)
        else:
            pass
        current_value = self.memory_usage_data[0]
        self.memory_usage_data = np.delete(self.memory_usage_data, 0)
        
        self.memory_usage = current_value
        LogLine.update_status('RAM usage', RESULT_FILE_LOCATION)
    
    @task
    def send_request(self):
        """After taking the neccessary infor, execute main task"""
        response = self.client.request(
            method = 'GET',
            url = f'/?value={self.execution_time}&memory={self.memory_usage}'
        )

        # Analyse all measurement information
        response_body = response.text.strip()
        lines = response_body.split('\n')
        first_line = lines[0].split(',')
        input_execution_time = first_line[0].split()[1]
        input_ram_usage = first_line[1].split()[1]
        real_ram_usage = lines[1].split()[2]
        response_time = response.elapsed.total_seconds()
        response_time = response_time * 1000
        current_time = time()
        local_time = localtime(current_time)
        formatted_time = strftime("%H:%M:%S", local_time)
        
        # Use these information and insert into .csv file
        with open (f'{RESULT_FILE_LOCATION}', mode = 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                AdvanceCurlTask.RESULT_LINE_COUNT,
                input_execution_time,
                input_ram_usage,
                response_time,
                real_ram_usage,
                formatted_time
                ])

        # Adjust line count for csv file
        AdvanceCurlTask.RESULT_LINE_COUNT += 1


class AdvanceCurlUser(HttpUser):
    """Define User to execute AdvanceCurlTAsk"""
    tasks = [AdvanceCurlTask]
    host = 'http://localhost:28080/mem.php'
    
    def wait_time(self):
        """Define own wait time"""
        return AdvanceCurlTask.time_between_task
  
@events.init.add_listener
def on_init():
    """Execute on initiation"""
    os.system(f'touch {RESULT_FILE_LOCATION}')