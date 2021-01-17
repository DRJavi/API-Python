import os
import json

from todos import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')
trans = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True);


def translate(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    
    xjson = json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
                           
    xpython = json.loads(xjson)
    
    xjsonResult = xpython.dumps(xpython)
    
    xresult = trans.translate_text(Text=xpython["text"], SourceLanguageCode="en", TargetLanguageCode="de")

    print (xresult)
    
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(xjsonResult,
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
