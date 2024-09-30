"""
Module for analysing data
"""
import csv
import numpy as np

class GenerateData:
    """Generate data based on .csv file"""
    @staticmethod
    def memory_data(app_id, file):
        """Memory data"""
        
        with open(file, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if row[1] == app_id:
                    pct1 = float(row[4])
                    pct5 = float(row[5])
                    pct25 = float(row[6])
                    pct50 = float(row[7])
                    pct75 = float(row[8])
                    pct95 = float(row[9])
                    pct99 = float(row[10])
                    pct100 = float(row[11])
                    # average = float(row[3])
                    sample_count = int(row[2])  # Ensure sample_count is an integer
                    break
        
        count_pct1 = int(sample_count * 0.01)               # 1% below pct1
        count_pct5 = int(sample_count * (0.05 - 0.01))      # 5% below pct5
        count_pct25 = int(sample_count * (0.25 - 0.05))     # 25% below pct25
        count_pct50 = int(sample_count * (0.50 - 0.25))     # 50% below pct50
        count_pct75 = int(sample_count * (0.75 - 0.50))     # 75% below pct75
        count_pct95 = int(sample_count * (0.95 - 0.75))     # 95% below pct95
        count_pct99 = int(sample_count * (0.99 - 0.95))     # 99% below pct99
        count_pct100 = sample_count - (count_pct1 + count_pct5 + count_pct25 + count_pct50 + count_pct75 + count_pct95 + count_pct99)

        # Generate random data for each percentile
        data_pct1 = np.random.uniform(0, pct1, count_pct1)               # Uniform between 0 and pct1
        data_pct5 = np.random.uniform(pct1, pct5, count_pct5)            # Uniform between pct1 and pct5
        data_pct25 = np.random.uniform(pct5, pct25, count_pct25)         # Uniform between pct5 and pct25
        data_pct50 = np.random.uniform(pct25, pct50, count_pct50)        # Uniform between pct25 and pct50
        data_pct75 = np.random.uniform(pct50, pct75, count_pct75)        # Uniform between pct50 and pct75
        data_pct95 = np.random.uniform(pct75, pct95, count_pct95)        # Uniform between pct75 and pct95
        data_pct99 = np.random.uniform(pct95, pct99, count_pct99)        # Uniform between pct95 and pct99
        data_pct100 = np.random.uniform(pct99, pct100, count_pct100)     # Uniform between pct99 and pct100

        # Combine the data from all percentiles
        data = np.concatenate([data_pct1, data_pct5, data_pct25, data_pct50, data_pct75, data_pct95, data_pct99, data_pct100])
        np.random.shuffle(data)
        
        return data
            
    @staticmethod
    def durations_data(app_id, file):
        """Function duration data"""
        
        with open(file, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if row[1] == app_id:
                    pct1 = float(row[8])
                    pct25 = float(row[9])
                    pct50 = float(row[10])
                    pct75 = float(row[11])
                    pct99 = float(row[12])
                    pct100 = float(row[13])
                    count = int(row[4])
                    min_value = float(row[5])
                    max_value = float(row[6])
                    break
                
        count = count - 2
        count_pct1 = int(count * 0.01)                    # 5% below pct1
        count_pct25 = int(count * (0.25 - 0.01))          # 25% below pct25
        count_pct50 = int(count * (0.50 - 0.25))          # 50% below pct50
        count_pct75 = int(count * (0.75 - 0.50))          # 75% below pct75
        count_pct99 = int(count * (0.99 - 0.75))          # 99% below pct99
        count_pct100 = count - (count_pct1 + count_pct25 + count_pct50 + count_pct75 + count_pct99)  # Remaining to pct100

        # Generate random data for each percentile using uniform distribution
        data_min = np.random.uniform(min_value, min_value, 1)
        data_max = np.random.uniform(max_value, max_value, 1)
        data_pct1 = np.random.uniform(min_value, pct1, count_pct1)              # Between pct0 and pct1
        data_pct25 = np.random.uniform(pct1, pct25, count_pct25)                # Between pct1 and pct25
        data_pct50 = np.random.uniform(pct25, pct50, count_pct50)               # Between pct25 and pct50
        data_pct75 = np.random.uniform(pct50, pct75, count_pct75)               # Between pct50 and pct75
        data_pct99 = np.random.uniform(pct75, pct99, count_pct99)               # Between pct75 and pct99
        data_pct100 = np.random.uniform(pct99, pct100, count_pct100)            # Above pct99 to maximum

        # Combine the data from all percentiles
        data = np.concatenate([data_pct1, data_pct25, data_pct50, data_pct75, data_pct99, data_pct100, data_min, data_max])
        np.random.shuffle(data)
        
        return data
    
def main():
    # try:
    #     data = GenerateData.durations_data('7ca324d9fc836a5d4562811c11ce3719530ee919dd1fb91bcaf71942eab8240a', '../../azure-sampleData/function_durations/function_durations_percentiles.anon.d01.csv')
    #     print("Generated data for '7ca324d9fc836a5d4562811c11ce3719530ee919dd1fb91bcaf71942eab8240a'")
    #     print(type(data))
    # except ValueError as e:
    #     print(e)
        
    try:
        data = GenerateData.memory_data('7ca324d9fc836a5d4562811c11ce3719530ee919dd1fb91bcaf71942eab8240a', '../../azure-sampleData/app_memory/app_memory_percentiles.anon.d01.csv')
        print("Generated data for '7ca324d9fc836a5d4562811c11ce3719530ee919dd1fb91bcaf71942eab8240a'")
        print(type(data))
    except ValueError as e:
        print(e)
    
if __name__ == '__main__':
    main()

  