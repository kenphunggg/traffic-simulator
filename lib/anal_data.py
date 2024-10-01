from time import time, localtime, strftime
import requests

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


if __name__ == '__main__':
    
    url = 'http://localhost:28080/mem.php/?value=2&memory=5'
    response_info = requests.get(url)
    print(AnalyzeData.get_response(response_info, "analyzed_at"))
