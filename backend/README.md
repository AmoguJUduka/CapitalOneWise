# CapitalOneWise – Smart Budget Tracker (Backend)

CapitalOneWise is a serverless financial microservice built on AWS, designed as part of a portfolio project for the **Capital One Developer Academy (CODA)**. This backend enables users to:

- Log expenses by category
- Set monthly budgets
- Receive automatic overspending alerts
- Schedule weekly budget checks with notifications

---

## 🏗️ Architecture

![Backend Architecture](Backend%20Architecture.png)

**Components:**
- **API Gateway**: Exposes two REST endpoints: `/add-expense` and `/add-budget`
- **Lambda Functions**:
  - `AddExpenseFunction`: Stores user expenses in DynamoDB
  - `AddBudgetFunction`: Stores monthly budget settings
  - `CheckBudgetsFunction`: Compares total spending vs budgets and publishes alerts
- **DynamoDB Tables**:
  - `ExpensesTable`: Stores each individual expense entry
  - `BudgetsTable`: Stores monthly budgets per user/category
- **SNS Topic**:
  - `OverspendAlerts`: Sends alerts to subscribed users when budgets are exceeded
- **EventBridge**:
  - Triggers weekly execution of `CheckBudgetsFunction`

---

## 📦 Tech Stack

| Layer             | Service Used             |
|------------------|--------------------------|
| Compute           | AWS Lambda (Python 3.11) |
| API Gateway       | REST Interface           |
| Database          | Amazon DynamoDB          |
| Notification      | Amazon SNS               |
| Scheduling        | Amazon EventBridge       |
| IaC               | AWS SAM + CloudFormation |

---

## 🛠️ How It Works

### 1. Add Expense
- Endpoint: `POST /add-expense`
- Payload:
```json
{
  "user_id": "user123",
  "category": "Groceries",
  "amount": 75,
  "date": "2025-07-10",
  "description": "Walmart trip"
}
```

### 2. Add Budget
- Endpoint: `POST /add-budget`
- Payload:
```json
{
  "user_id": "user123",
  "category": "Groceries",
  "monthly_budget": 300
}
```

### 3. Weekly Budget Check
- Triggered every Sunday 8 AM UTC
- Compares total expenses per category to the user's budget
- If over budget, sends an SNS alert email

---

## 🚨 Alerts

To receive alerts:
- Subscribe your email to the SNS topic: `OverspendAlerts`
```bash
aws sns subscribe \
  --topic-arn arn:aws:sns:<region>:<account>:OverspendAlerts \
  --protocol email \
  --notification-endpoint youremail@example.com
```

---

## 📁 Folder Structure

```
backend/
├── README.md
├── __init__.py
├── events
│   └── event.json
├── hello_world
│   ├── __init__.py
│   ├── add_budget.py     # Add budget logic
│   ├── app.py            # Add expense logic
│   ├── check_budget.py   # Weekly budget checker + SNS
│   └── requirements.txt
├── samconfig.toml        # Store configuration defaults for sam cli
├── template.yaml         # Defines infrasturcture for the serverless application
└── tests
    ├── __init__.py
    ├── integration
    │   ├── __init__.py
    │   └── test_api_gateway.py
    ├── requirements.txt
    └── unit
        ├── __init__.py
        └── test_handler.py
```

---

## 🚀 Deployment

```bash
sam build
sam deploy --guided
```

---

## 🔜 Coming Next

- React frontend (S3 + CloudFront)
- AWS Cognito authentication
- CI/CD pipeline with CodePipeline

---


