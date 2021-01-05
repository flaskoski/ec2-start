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
    #check if instance is currently in the stopped state
    if EC2INSTANCE.state['Name'] == 'stopped':
        EC2INSTANCE.start()
        LOGGER.info('Start InstanceID： ' + INSTANCE_ID)
        return
    else:
        LOGGER.info('InstanceID "' + INSTANCE_ID + '" is not stopped!')
