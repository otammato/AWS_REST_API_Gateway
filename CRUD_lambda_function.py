import json
import boto3

dynamo = boto3.resource("dynamodb")

table = dynamo.Table('http-crud-tutorial-items')

def handler(event, context):
  status_code = 200
  headers = {
      "Content-Type": "application/json"
  }
  if event['routeKey'] == "GET /items":
    response = table.scan()
    body = response["Items"]
  elif event["routeKey"] == "PUT /items":
    table.put_item(
    Item={"id": json.loads(event["body"])["id"],
          "name": json.loads(event["body"])["name"],
          "price": json.loads(event["body"])["price"]}
    )
    body = "item {} added in the table".format(json.loads(event["body"])["id"])
  elif event["routeKey"] == "DELETE /items/{id}":
    table.delete_item(
    Key={"id": event["pathParameters"]["id"]}
    )
    body = "Deleted item {} from the table".format(event['pathParameters']['id'])
  elif event["routeKey"] == "GET /items/{id}":
    responseDB = table.get_item(
        Key={"id": event["pathParameters"]["id"]}
    )
    if "Item" in responseDB:
      body = responseDB["Item"] 
    else:
      body = "Requested item does not exist in the table"

  return {"status_code" : status_code, "body" : body, "headers" : headers}
