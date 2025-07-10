import json
import uuid
import boto3
import os
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('EXPENSES_TABLE', 'ExpensesTable')
table = dynamodb.Table(table_name)

# Custom encoder to convert Decimal → float
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'], parse_float=Decimal)

        expense_item = {
            "expense_id": str(uuid.uuid4()),
            "user_id": body["user_id"],
            "category": body["category"],
            "amount": body["amount"],
            "date": body["date"],
            "description": body.get("description", "")
        }

        table.put_item(Item=expense_item)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Expense added successfully",
                "item": expense_item
            }, cls=DecimalEncoder),
            "headers": {
                "Content-Type": "application/json"
            }
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {
                "Content-Type": "application/json"
            }
        }

