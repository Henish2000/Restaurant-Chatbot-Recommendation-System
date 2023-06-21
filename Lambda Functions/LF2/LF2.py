import json
import random
import boto3
import logging
from botocore.exceptions import ClientError
import requests 

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def lambda_handler(event, context):
    checkSqs(event)

def checkSqs(event):
    msg_info = event['Records'][0]['messageAttributes']
    cuisine = msg_info['cuisine']['stringValue']
    location = msg_info['location']['stringValue']
    time = msg_info['time']['stringValue']
    people = msg_info['people']['stringValue']
    email = msg_info['email']['stringValue']
    rid = get_rest_id(cuisine)
    data = get_restaurant_info(rid)
    sendMessage = 'Hello! Here are my '+ cuisine +' restaurant suggestions for ' + people + ' people, at ' + time + " " + '\n' +data
    temp_email(sendMessage,email)

def get_rest_id(cuisine):
    es_query = "https://search-restaurants-g7ikxqgqdbmkt64tdwa7fci6v4.us-east-1.es.amazonaws.com/_search?q={cuisine}".format(
        cuisine=cuisine)
    esResponse = requests.get(es_query,auth=('aniketrest', 'London@1985'))
    data = json.loads(esResponse.content.decode('utf-8'))
    try:
        esData = data["hits"]["hits"]
    except KeyError:
        logger.debug("Error extracting hits from ES response")
    num = random.randint(0,len(esData)-1)
    tmpDict = esData[num]
    rid = tmpDict['_source']['restaurantID']
    return rid
    
def get_restaurant_info(rest_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('yelp-restaurants')
    response = table.get_item(
        Key={
            'id': rest_id
        }
    )
    response_item = response.get("Item")
    restaurant_name = response_item['restaurent_name']
    restaurant_address = response_item['address']
    restaurant_zipcode = response_item['zip_code']
    formatted_restaurant_info = (restaurant_name+" "+' ,'.join(restaurant_address))
    return formatted_restaurant_info
    
def temp_email(sendMessage,email):
    ses_client = boto3.client("ses", region_name="us-east-1")
    CHARSET = "UTF-8"
    ses_client.send_email(
        Destination={
            "ToAddresses": [
                email,
            ],
        },
        Message={
            "Body": {
                "Text": {
                    "Charset": CHARSET,
                    "Data": sendMessage,
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": "Dining Suggestions Chatbot",
            },
        },
        Source="aniketsaliya123@gmail.com",
    )