"""
Interact with csv files
"""
import csv
from time import time, localtime, strftime


    

class LogLine:
    """
    Get info needed to running tests
    """
    @staticmethod
    def invocations_update(trigger_per_minute, time_between_task, invocation_column, result_file):
        """
        Return update information of invocation file on update
        """
        with open (result_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([f"Trigger: {trigger_per_minute} times"])
            writer.writerow([f"Time between tasks: {time_between_task}"])
            writer.writerow([f"Current column: {invocation_column}"])
            writer.writerow(["Time between tasks updated"])
            
    @staticmethod
    def invocations_not_update(trigger_per_minute, time_between_task, invocations_column, result_file):
        """
        Return update information of invocation file on update
        """
        with open (result_file, mode = 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([f"Trigger: Remaining {trigger_per_minute} times"])
            # writer.writerow([f"Time between tasks: {time_between_task*4}"])
            writer.writerow([f"Time between tasks: {time_between_task}"])
            writer.writerow([f"Current column: {invocations_column}"])
            writer.writerow(["Time between tasks NOT updated"])
            
    @staticmethod
    def update_status(status, result_file):
        """
        Return status
        """
        with open (result_file,mode = 'a',newline='',encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([f"Update {status}"])
            
    @staticmethod
    def get_app_id(app_id, result_file):
        """
        Return status
        """
        with open (result_file,mode = 'a',newline='',encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([f"App ID: {app_id}"])
            
    @staticmethod
    def header(file):
        """
        Print header for csv file
        """
        with open (file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                "Line count", 
                "Input execution time(ms)", 
                "Input ram usage(MB)", 
                "Response time",
                "Real ram usage"
                ])
    
class FromTriggerRow:
    """
    Get data from the row you give
    """
    @staticmethod
    def get_app_id(desired_row, file):
        """
        Get trigger per minute with desired row
        """
        with open(file, mode='r', encoding='utf-8') as invocations_file:
                invocations_reader = csv.reader(invocations_file, delimiter=',')
                next(invocations_reader)
                row_count = 1
                for row in invocations_reader:
                    if row_count < desired_row:
                        row_count += 1
                    elif row_count == desired_row:
                        app_id = row[1]
                        break
                        
        return app_id
    
class GetData:
    """
    Get crucial information for running the test
    """
    @staticmethod
    def app_id(desire_app_count, file):
        """
        Get app id
        """
        current_row = 1
        temp_app_id = FromTriggerRow.get_app_id(desired_row=current_row,
                                                file=file)
        tracking_app_count = 1
        
        while True:
            if tracking_app_count < desire_app_count:
                current_app_id = FromTriggerRow.get_app_id(desired_row=current_row,
                                                           file=file)
                if current_app_id != temp_app_id:
                    temp_app_id = current_app_id
                    tracking_app_count += 1
                    current_row += 1
                elif current_app_id == temp_app_id:
                    current_row += 1
            elif tracking_app_count == desire_app_count:
                app_id = FromTriggerRow.get_app_id(desired_row=max(current_row-1, 1),
                                                   file=file)
                break
        return app_id
    
    @staticmethod
    def trigger_per_minute(app_id, column, file):
        """
        Get trigger per minute with app_id
        """
        with open(file, mode='r', encoding='utf-8') as invocations_file:
            invocations_reader = csv.reader(invocations_file, delimiter=',')
            next(invocations_reader)
            trigger_per_minute = 0
            first_time = 0
            for row in invocations_reader:
                if app_id == row[1]:
                    trigger_per_minute += float(row[column])
                    first_time = 1
                if app_id != row[1]:
                    if first_time == 1:
                        break
                # print(row[1])
                # print(app_id)
                # print("NEXT")
                        
        return trigger_per_minute
    
    @staticmethod
    def time_between_task(trigger_per_minute, step_time):
        """
        Get time between tasks based on trigger per minute
        """
        if trigger_per_minute == 0:
            time_between_task = step_time
        else:
            time_between_task = step_time/trigger_per_minute
            
        return time_between_task
            
            
           

class AnalyzeData:
    """Analyzing data from a response object"""
    
    @staticmethod
    def get_response(response, key=None):
        """
        Analyzing response data from a HTTP request GET
        """
        response_body = response.text.strip()
        lines = response_body.split('\n')
        
        # Extracting the necessary information
        first_line = lines[0].split(',')
        input_execution_time = first_line[0].split()[1]
        input_ram_usage = first_line[1].split()[1]
        real_ram_usage = lines[1].split()[2]
        
        # Calculating response time in milliseconds
        response_time = response.elapsed.total_seconds() * 1000
        
        # Getting current local time
        current_time = time()
        local_time = localtime(current_time)
        formatted_time = strftime("%H:%M:%S", local_time)
        result = {
            "input_execution_time": input_execution_time,
            "input_ram_usage": input_ram_usage,
            "real_ram_usage": real_ram_usage,
            "response_time": response_time,
            "formatted_time": formatted_time
        }
        
        if key:
            return result.get(key, f"Key '{key}' not found")
        else:
            return result
    
    
if __name__ == "__main__":
    PARENT_FILE_LOCATION = 'azure-sampleData'
    CHILD_FILE_LOCATION = 'invocations'
    FILE_LOCATION = 'invocations_per_function_md.anon.d01.csv'
    app_id_test = GetData.app_id(desire_app_count=3,
                              file=f'../../{PARENT_FILE_LOCATION}/{CHILD_FILE_LOCATION}/{FILE_LOCATION}')
    print(app_id_test)
    tpm_test = GetData.trigger_per_minute(app_id=app_id_test,
                                          column=4,
                                          file=f'../../{PARENT_FILE_LOCATION}/{CHILD_FILE_LOCATION}/{FILE_LOCATION}')
    print(tpm_test)
    
    