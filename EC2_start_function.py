import logging
import os
import sys
import boto3

LOGGER = logging.getLogger()
for h in LOGGER.handlers:
    LOGGER.removeHandler(h)

HANDLER = logging.StreamHandler(sys.stdout)
FORMAT = '%(levelname)s %(asctime)s [%(filename)s:%(funcName)s:%(lineno)d] %(message)s'
HANDLER.setFormatter(logging.Formatter(FORMAT))
LOGGER.addHandler(HANDLER)
LOGGER.setLevel(logging.INFO)

# get environment variable
INSTANCE_ID = os.environ['INSTANCE_ID']

EC2 = boto3.resource('ec2')
EC2INSTANCE = EC2.Instance(INSTANCE_ID)
EC2CLIENT = EC2.meta.client


def main(event, context):
    """
    main function
    """
    try:
        startEC2()
    except Exception as error:
        LOGGER.exception(error)

def startEC2():
    response = EC2CLIENT.describe_instance_status(InstanceIds=[INSTANCE_ID])
    instance_status = response['InstanceStatuses'][0]['InstanceStatus']['Status']
    system_status = response['InstanceStatuses'][0]['SystemStatus']['Status']

    if instance_status == 'initializing' or system_status == 'initializing':
        LOGGER.info('Aborts. Currently InstanceStatus Checking')
        return
    #check if instance is currently in the stopped state
    elif EC2INSTANCE.state['Name'] == 'stopped':
        EC2INSTANCE.start()
        LOGGER.info('Start InstanceID： ' + INSTANCE_ID)
        #wait for the EC2 instance to go to running state
        EC2CLIENT.get_waiter('instance_running').wait(
            InstanceIds=[
                INSTANCE_ID
            ],
            WaiterConfig={
                'Delay': 5,  # Default: 15
                'MaxAttempts': 20  # Default: 40
            }
        )
        LOGGER.info("Completed!")
        return
    else:
        LOGGER.info('InstanceID "' + INSTANCE_ID + '" is not stopped!')
