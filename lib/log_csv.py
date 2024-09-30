"""
Interact with csv files
"""
import csv

    

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
            writer.writerow([f"Time between tasks: {time_between_task*4}"])
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
            writer.writerow([f"Time between tasks: {time_between_task*4}"])
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
            
class ReadCSV:
    """
    Get needed info
    """
    @staticmethod
    def trigger_per_minute(file, desired_row, column):
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
                    trigger_per_minute = float(row[column])
                    break
                        
        return trigger_per_minute
    
    @staticmethod
    def time_between_task(trigger_per_minute, step_time):
        """
        Get time between tasks based on trigger per minute
        """
        if trigger_per_minute == 0:
            time_between_task = step_time/2
        else:
            time_between_task = step_time/trigger_per_minute/4
            
        return time_between_task
    
    @staticmethod
    def app_id(file, desired_row):
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
    
    
    