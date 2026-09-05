RecoverAI

AI-Powered Revenue Recovery for Failed Payments

RecoverAI is an AI-powered revenue recovery system built for the
Razorpay Buildathon -- AI Revenue Recovery track.

A failed payment does not always mean lost revenue.

Instead of treating every failed transaction the same way or repeatedly
retrying payments using fixed rules, RecoverAI analyzes the transaction,
estimates its probability of recovery, and recommends the most
appropriate next action.

The system combines Machine Learning + a Decision Engine + Risk/Policy
Rules + Recovery Tracking to make recovery decisions more
intelligently.

Problem

Payment failures are a common part of digital payments.

A transaction can fail because of:

Temporary bank declines

Insufficient funds

Network or timeout issues

Authentication failures

Payment method problems

Other temporary or customer-specific conditions

Traditional recovery approaches often treat these failures using fixed
rules:

Payment Failed
      ↓
Retry
      ↓
Retry Again
      ↓
Retry Again
      ↓
Customer gives up

This can lead to recoverable payments being lost and unnecessary
repeated attempts.

The key question is:

Is this failed payment worth recovering, and what should we do
next?

Our Approach

RecoverAI treats payment recovery as a decision-making problem.

Failed Payment
      ↓
Transaction & Customer Data
      ↓
Machine Learning Model
      ↓
Recovery Probability
      ↓
Decision Engine + Risk/Policy Rules
      ↓
Smart Retry OR Escalate / Manual Review
      ↓
Recovery Outcome
      ↓
Audit / Decision History
      ↓
Revenue Dashboard

The goal is not simply to predict whether a payment will recover. The
goal is to use that prediction to make a practical recovery decision.

Key Features

1. AI-Based Recovery Prediction

RecoverAI uses a Machine Learning model to estimate the probability that
a failed payment can be recovered.

Example:

Recovery Probability: 75.8%
Recommended Action: Smart Retry
Decision: Suitable for automated recovery

2. Customer Behaviour Signals

The system considers:

Previous successful payments

Previous failed payments

Customer Lifetime Value

Days since last successful payment

Retry count

3. Transaction & Payment Signals

RecoverAI also considers:

Transaction amount

Failure reason

Payment method

Checkout duration

Risk score

Number of previous retries

4. Decision Engine

The ML model produces a recovery probability, but it does not make the
final decision alone.

The Decision Engine combines:

ML Prediction
     +
Risk Signals
     +
Retry Policy
     +
Transaction Context
     ↓
Final Recovery Decision

Possible outcomes include:

smart_retry

escalate

manual_review

5. Recovery Execution

When a transaction meets the configured recovery conditions, RecoverAI
allows the recommended recovery action to be executed.

In the current prototype, recovery execution is simulated. The
system updates the transaction state and recovered amount to demonstrate
the complete workflow.

Important: The current hackathon prototype does not claim to move
real money through Razorpay.

The architecture can later be connected to Razorpay Test Mode / payment
APIs.

6. Audit / Decision History

The system records:

Transaction ID

Amount

Recovery probability

Recommended action

Current status

Amount recovered

7. Revenue Recovery Dashboard

The dashboard displays:

Total transactions

Total transaction value

Average recovery probability

Recovered revenue

Recovery rate

High recovery opportunities

Recommended actions

AI engine status

Machine Learning

Dataset

For the prototype, we generated a synthetic dataset of approximately
5,000 transaction records representing different payment failure and
customer behaviour scenarios.

The features include:

Transaction amount

Failure reason

Previous successes

Previous failures

Customer Lifetime Value

Retry count

Days since last payment

Checkout duration

Payment method

Risk score

Recovery outcome

Real payment data was not used because payment transaction data is
private.

Model Selection

We experimented with:

Logistic Regression

Random Forest

After comparison, Logistic Regression was selected for the
prototype.

Approximate evaluation results:

ROC-AUC: 0.704

F1 Score: 0.591

The model is intentionally lightweight for faster inference, easier
debugging, interpretability, and easier explanation during the
hackathon.

Why Machine Learning + Rules?

Machine Learning answers:

"What is the probability of recovery?"

The Decision Engine then asks:

"Is it safe and appropriate to act?"

Machine Learning
      ↓
Recovery Probability
      ↓
Decision Engine
      ↓
Risk + Policy Checks
      ↓
Recovery Action

This separation makes the system more practical than relying on a model
prediction alone.

Example

A potentially recoverable transaction:

Transaction Amount: ₹10,000
Failure Reason: Temporary Bank Decline
Previous Successes: 8
Previous Failures: 1
Customer Lifetime Value: ₹75,000
Retry Count: 1
Risk Score: 0.25

Possible result:

Recovery Probability: ~75%
Action: Smart Retry
Decision: Recommended

After simulated execution:

Status: EXECUTED
Amount Recovered: ₹10,000

A higher-risk transaction with repeated failures may instead receive:

Action: Escalate
Status: Pending

This demonstrates the core idea of intelligent recovery.

System Architecture

                    ┌──────────────────────┐
                    │     Failed Payment   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Transaction Features │
                    │ Customer History     │
                    │ Risk Signals         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   ML Prediction      │
                    │ Logistic Regression  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Decision Engine    │
                    │ Risk + Policy Rules  │
                    └──────────┬───────────┘
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
             ┌──────────────┐      ┌──────────────┐
             │ Smart Retry  │      │   Escalate   │
             └──────┬───────┘      └──────┬───────┘
                    │                     │
                    └──────────┬──────────┘
                               ▼
                    ┌──────────────────────┐
                    │ Recovery Outcome     │
                    └──────────┬───────────┘
                               ▼
                    ┌──────────────────────┐
                    │ Audit / Decision Log │
                    └──────────┬───────────┘
                               ▼
                    ┌──────────────────────┐
                    │ Revenue Dashboard    │
                    └──────────────────────┘

Technology Stack

Frontend

React

Vite

JavaScript / JSX

CSS

Lucide Icons

Backend

Python

FastAPI

Uvicorn

SQLAlchemy

SQLite

Machine Learning

Pandas

NumPy

Scikit-learn

Joblib

Development

VS Code

Git

GitHub

Project Structure

RecoverAI/
├── backend/
│   ├── agent/
│   │   ├── decision_engine.py
│   │   └── audit.py
│   ├── app/
│   │   ├── database.py
│   │   └── models.py
│   ├── ml/
│   │   ├── data/
│   │   ├── model/
│   │   ├── generate_data.py
│   │   └── train_model.py
│   ├── services/
│   │   └── recovery_agent.py
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── ...
│   ├── package.json
│   └── vite.config.js
│
└── README.md

API Endpoints

Method   Endpoint                    Purpose

GET      /                         API information
GET      /health                   Backend health check
POST     /analyze                  Analyze a failed transaction
GET      /transactions             Get transaction history
GET      /transactions/{case_id}   Get a specific transaction
POST     /recover/{case_id}        Execute simulated recovery
GET      /stats                    Get recovery statistics
GET      /audit-log                Get decision history

Running Locally

Backend

cd backend
python -m venv .venv
.venv\Scriptsctivate
pip install -r requirements.txt
python -m uvicorn main:app --reload

Backend:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

Frontend

Open another terminal:

cd frontend
npm install
npm run dev

Frontend:

http://localhost:5173

Demo Flow

Dashboard --- View transaction volume, transaction value,
recovery probability, recovered revenue and recovery rate.

Transactions --- View failed transactions and their recovery
states.

AI Analysis --- Enter a failed transaction and run the AI
analysis.

Recovery Execution --- Execute an approved recovery action in
the prototype.

Audit Log --- Review the decision history and recovery outcome.

What Makes RecoverAI Different?

Traditional approach:

Payment Failed
      ↓
Retry

RecoverAI:

Payment Failed
      ↓
Understand Context
      ↓
Predict Recovery Probability
      ↓
Evaluate Risk & Policy
      ↓
Choose Appropriate Action
      ↓
Recover or Escalate
      ↓
Track Outcome

The focus is on recovery quality rather than simply increasing the
number of retries.

Current Prototype Limitations

Synthetic Data

The model is trained on synthetic transaction data rather than real
Razorpay customer data.

Simulated Recovery

The /recover endpoint simulates recovery execution and updates the
database. It does not perform real-money transactions.

Rule-Based Policy Layer

The current decision engine uses configured rules alongside the ML
prediction.

Local Database

SQLite is used for simplicity during development. A production version
could use PostgreSQL or another scalable database.

Future Scope

Razorpay Integration

Connect the recovery execution layer with Razorpay APIs and Test Mode.

Real Transaction Data

Train the model using anonymized historical payment data.

Better Recovery Strategies

Learn which recovery strategy works best for different failure types.

Temporary Bank Decline → Smart Retry
Insufficient Funds      → Delayed Retry / Customer Prompt
Repeated Failure        → Escalation
High-Risk Transaction   → Manual Review

Continuous Learning

Feed recovery outcomes back into the training pipeline so the model can
improve over time.

Real-Time Monitoring

Consume payment failure events in real time and automatically analyze
them.

Hackathon Context

RecoverAI was developed as a hackathon prototype for the Razorpay
Buildathon -- AI Revenue Recovery challenge.

The project focuses on a practical question:

How can failed payments be turned into recoverable revenue without
blindly retrying every transaction?

Final Takeaway

RecoverAI aims to move payment recovery from:

"Retry everything."

to:

"Understand the failure. Predict the opportunity. Choose the right
action."

RecoverAI

Predict. Decide. Recover.
