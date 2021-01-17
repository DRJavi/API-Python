import os
import json

from todos import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')
trans = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True);
comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')


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
    
    text = xpython["text"]
    dominantLen = comprehend.detect_dominant_language(Text = text).get('Languages')[0].get('LanguageCode')
    
    textTrad = trans.translate_text(Text=xpython["text"], SourceLanguageCode=dominantLen, TargetLanguageCode=event['pathParameters']['le'])
    outputText = textTrad.get('TranslatedText')
    
    xpython["text"] = outputText

    
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(xpython)
    }

    return response
