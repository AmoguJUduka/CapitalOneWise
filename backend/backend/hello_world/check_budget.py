import json
import boto3
import os
from decimal import Decimal
from collections import defaultdict
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

expenses_table = dynamodb.Table(os.environ['EXPENSES_TABLE'])
budgets_table = dynamodb.Table(os.environ['BUDGETS_TABLE'])
sns_topic_arn = os.environ['SNS_TOPIC_ARN']

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

def lambda_handler(event, context):
    try:
        # Step 1: Get all expenses
        scan_expenses = expenses_table.scan()
        expenses = scan_expenses['Items']

        # Step 2: Aggregate spending per user/category
        totals = defaultdict(Decimal)
        for item in expenses:
            key = (item['user_id'], item['category'])
            totals[key] += item.get('amount', Decimal('0'))

        # Step 3: Check each against the user's budget
        alerts = []
        for (user_id, category), spent in totals.items():
            response = budgets_table.get_item(
                Key={"user_id": user_id, "category": category}
            )
            budget_item = response.get("Item")
            if budget_item:
                budget = budget_item['monthly_budget']
                if spent > budget:
                    alerts.append({
                        "user_id": user_id,
                        "category": category,
                        "spent": float(spent),
                        "budget": float(budget)
                    })

        # Step 4: Send alert if needed
        if alerts:
            message = {
                "alerts": alerts,
                "summary": f"{len(alerts)} categories over budget"
            }
            sns.publish(
                TopicArn=sns_topic_arn,
                Subject="🚨 Budget Alert: Overspending Detected",
                Message=json.dumps(message, cls=DecimalEncoder)
            )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Budget check complete",
                "alerts_sent": len(alerts)
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
