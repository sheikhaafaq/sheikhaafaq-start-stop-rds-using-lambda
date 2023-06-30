import os
import boto3
import json
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    
    # Fetch Datebase Identifier Environment variable
    DBinstance = os.environ['DBInstanceName']
    
    #create an Rds client
    context.rds_client = boto3.client('rds')
   
    # Describe instance
    response = context.rds_client.describe_db_instances(DBInstanceIdentifier=DBinstance )

    #Check the status of rds instance
    status = response['DBInstances'][0]['DBInstanceStatus']

    # If Rds Instance is in stopped stop, It will be started
    if status == "stopped":
        try:
        
            #Stopping the Rds instance
            response = context.rds_client.start_db_instance( DBInstanceIdentifier=DBinstance )
        
            #send logs to cloudwatch
            print ('Success :: Starting Rds instance:', DBinstance)
        
            #Logs to Lambda function Execution results
            return {
                'statusCode': 200,
                'message': "Starting Rds instance",
                'body': json.dumps(response, default=str)
            }
        
        except ClientError as e:
            #send logs to cloudwatch
            print(e)
            message = e
        
        #Logs to Lambda function Execution results
        return {
            'message': "Script execution completed. See Cloudwatch logs for complete output, but instance starting failed",
            'body': json.dumps(message, default=str)
        }
    # if Rds instance is in running state, It will be stopped
    elif status == "available":
        try: 
            #Stopping the Rds instance
            response = context.rds_client.stop_db_instance( DBInstanceIdentifier=DBinstance )
        
            #send logs to cloudwatch
            print ('Success :: Stopping Rds instance:', DBinstance)
        
            #Logs to Lambda function Execution results
            return {
                'statusCode': 200,
                'message': "Stopping Rds instance",
                'body': json.dumps(response, default=str)
            }
        except ClientError as e:
            #send logs to cloudwatch
            print(e)
            message = e
        
        #Logs to Lambda function Execution results
        return {
            'message': "Script execution completed. See Cloudwatch logs for complete output, but instance stopping failed",
            'body': json.dumps(message, default=str)
        }
