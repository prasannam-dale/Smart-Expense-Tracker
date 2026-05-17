import pandas as pd

def monthly_summary():
    try:
        df = pd.read_csv('data/expenses.csv')

        if df.empty:
            return None

        required_columns = [
            'date',
            'description',
            'amount',
            'category'
        ]

        for column in required_columns:
            if column not in df.columns:
                return None

        summary = df.groupby('category')['amount'].sum()

        return summary

    except Exception:
        return None


def predict_next_month_budget():
    try:
        df = pd.read_csv('data/expenses.csv')

        if df.empty:
            return 0

        total = df['amount'].sum()

        average = total / max(len(df), 1)

        prediction = average * 30

        return round(prediction, 2)

    except Exception:
        return 0