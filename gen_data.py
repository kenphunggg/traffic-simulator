import csv
import numpy as np

# Set the parameters
lambda_value = 5  # Average rate (mean) of occurrences
num_requests = 10  # Number of requests (rows)
num_samples_per_request = 300  # Number of samples per request (columns)

# Open the CSV file for writing
with open('poisson_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write the header row (optional)
    header = ['Request'] + [f'{i+1}' for i in range(num_samples_per_request)]
    writer.writerow(header)
    
    # Generate Poisson-distributed data for each request and write to CSV
    for i in range(1, num_requests + 1):
        data = np.random.poisson(lambda_value, num_samples_per_request)
        row = [i] + data.tolist()
        writer.writerow(row)

print("Data has been written to poisson_data.csv")
