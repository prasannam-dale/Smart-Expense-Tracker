import uuid
import csv
import os
from datetime import datetime
import pandas as pd

CSV_FILE = 'data/expenses.csv'

def load_expenses():
    return pd.read_csv(CSV_FILE)

def initialize_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                'id',
                'date',
                'description',
                'amount',
                'category'
            ])


def save_expense(description, amount, category):
    with open(CSV_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            str(uuid.uuid4()),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            description,
            amount,
            category
        ])

def delete_expense(expense_id):
    df = pd.read_csv(CSV_FILE)

    df = df[df["id"] != expense_id]

    df.to_csv(CSV_FILE, index=False)

def update_expense(expense_id, description, amount, category):
    df = pd.read_csv(CSV_FILE)

    df.loc[df["id"] == expense_id, "description"] = description
    df.loc[df["id"] == expense_id, "amount"] = amount
    df.loc[df["id"] == expense_id, "category"] = category

    df.to_csv(CSV_FILE, index=False)