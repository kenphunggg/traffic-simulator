# Simulating traffic based on an Azure Datatrace using Locust

## Installation

Make sure you have installed python modules in your device

```bash
apt install python3.11 python3.11-venv python3-pip
```

It is recommended to deploy locust into a python virtual environment

```bash
python3.11 -m venv traffic-simulator-venv
source traffic-simulator-venv/bin/activate
```

Then install locust and other dependencies on your virtual environment

```bash
pip install locust
pip install numpy
```

## Set up variables

Let's take a look at `multi_user.py`, adjust the variable below
`TEST_CASE` and `RESULT_FILE` are the subfile location of `result_file` in your repository and your file name, respectively
`INVOCATION_FILE_LOCATION`, `DURATION_FILE_LOCATION`, `MEMORY_FILE_LOCATION` are three .csv file location that we take from AzureDataTrace, which give us all information to simulate the traffic

```python
########## RESULT CONFIG ##############

TEST_CASE = 'test_case'
RESULT_FILE = 'test'

############ FILE LOCATION #############

INVOCATION_FILE_LOCATION = '../azure-sampleData/invocations/invocations_per_function_md.anon.d01.csv'
DURATION_FILE_LOCATION = '../azure-sampleData/function_durations/function_durations_percentiles.anon.d01.csv'
MEMORY_FILE_LOCATION = '../azure-sampleData/app_memory/app_memory_percentiles.anon.d01.csv'

###### SET UP BASED ON DATATRACE ######

STEP_TIME = 4

########################################
```

## Generate the file for running

I have trouble creating more than one user which follow the datatrace's rule, so i use `gen_code.py` clone the Class `User` for me and save in `NEW_FILE`

```bash
USER_COUNT = 5
NEW_FILE = genfile
python3 gencode.py $NEW_FILE $USER_COUNT
```

## Running the test

```bash
SPAWN_RATE = 100 # Users/second
locust -f genfile.py --headless -u $USER_COUNT -r $SPAWN_RATE
```







