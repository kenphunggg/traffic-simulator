# Simulating traffic based on an Azure Functions Trace using Locust

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
pip install -r requirements.txt
```

The app use to simulate the functions are taken from [workload-app](https://github.com/bonavadeur/workload-app)

## Download datatrace

The data we use for simulating are taken from [Azure Functions Trace](https://github.com/Azure/AzurePublicDataset/blob/master/AzureFunctionsDataset2019.md)

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

## Running the test

### Reset setup

Before running the test, run `del.sh` to reset (if you have run the test before)

```bash
chmod +x del.sh
./del.sh
```

### Setup

Setup the containers for testing

```bash
chmod +x run.sh
export USER_COUNT=50   # Specify the number of user
./run.sh $USER_COUNT
```

### Run the test
```bash
locust -f runtest.py --headless -u $USER_COUNT -r $USER_COUNT 
```







