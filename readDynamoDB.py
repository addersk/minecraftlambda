import boto3
import json

def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")
    
    table = dynamodb.Table('GameVersions')
    
    game = "Minecraft"
    version = "1.15.2"
    
    try:
        response = table.get_item(
            Key={
                'Game': game,
                'Version': version
            }
        )
    except:
        return {
            'statusCode': 500,
            'body': "Unable to lookup Minecraft version information."
        }
    else:
        item = response['Item']

        return {
            'statusCode': 200,
            'body': json.dumps(item)
        }
        
    return {
        'statusCode': 500,
        'body': "Unable to lookup Minecraft version information."
    }
