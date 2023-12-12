from google.cloud.sql.connector import Connector
import pg8000
import sqlalchemy
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
        
def calculate_total_expenditure_latest_month(pool, username):
    
    current_date = datetime.now()
    latest_month_to_check = current_date.month
    total_expenditure = 0.0
    
    query = sqlalchemy.text("""
    SELECT date, total_amount
    FROM receipt_details_2
    WHERE username = :username
    """)
    
    result = pool.execute(query, {"username": username}).fetchall()

    for row in result:
        latest_year = int(row['date'].split("-")[0])
        latest_month = int(row['date'].split("-")[1])
        
        print(f"latest month is: {latest_month} and latest year is: {latest_year}")
        
        if latest_month == latest_month_to_check:
            total_expenditure += float(row['total_amount'])
            

    total_expenditure = round(total_expenditure, 2)
    print(f"Total expenditure for user {username}: {total_expenditure}")
    
    return total_expenditure
    
def calculate_category_wise_expenditure_latest_month(pool, username):
    current_date = datetime.now()
    latest_month_to_check = current_date.month

    query = sqlalchemy.text("""
        SELECT category, date, total_amount
        FROM receipt_details_2
        WHERE username = :username
    """)

    result = pool.execute(query, {"username": username}).fetchall()

    category_wise_expenditure = {}

    for row in result:
        year = int(row['date'].split("-")[0])
        month = int(row['date'].split("-")[1])

        if month == latest_month_to_check:
            category = row['category']
            total_amount = float(row['total_amount'])

            if category not in category_wise_expenditure:
                category_wise_expenditure[category] = 0.0

            category_wise_expenditure[category] += total_amount

    return category_wise_expenditure


def get_latest_transaction_details(pool, username):
    query = sqlalchemy.text("""
        SELECT category, merchant_name, CONCAT(city, ', ', state) as location, date, total_amount
        FROM receipt_details_2
        WHERE username = :username
        ORDER BY date DESC
        LIMIT 5
    """)

    result = pool.execute(query, {"username": username}).fetchall()

    transaction_details = []
    for row in result:
        transaction_details.append({
            'category': row['category'],
            'merchant_name': row['merchant_name'],
            'location': row['location'],
            'date': row['date'],
            'total_amount': row['total_amount']
        })

    return transaction_details

def calculate_highest_spending_category_latest_month(pool, username):
    current_date = datetime.now()
    latest_month_to_check = current_date.month

    query = sqlalchemy.text("""
        SELECT category, date, total_amount
        FROM receipt_details_2
        WHERE username = :username
    """)

    result = pool.execute(query, {"username": username}).fetchall()

    category_wise_expenditure = {}

    for row in result:
        year = int(row['date'].split("-")[0])
        month = int(row['date'].split("-")[1])

        if month == latest_month_to_check:
            category = row['category']
            total_amount = float(row['total_amount'])

            if category not in category_wise_expenditure:
                category_wise_expenditure[category] = 0.0

            category_wise_expenditure[category] += total_amount

    highest_spending_category = max(category_wise_expenditure, key=category_wise_expenditure.get, default=None)
    return highest_spending_category

def monthly_expenditure_trends(pool, username):
    query = sqlalchemy.text("""
        SELECT date, total_amount
        FROM receipt_details_2
        WHERE username = :username
    """)

    result = pool.execute(query, {"username": username}).fetchall()

    # Convert the result to a Pandas DataFrame
    df = pd.DataFrame(result, columns=['date', 'total_amount'])

    # Convert the 'date' column to datetime type
    df['date'] = pd.to_datetime(df['date'])

    # Extract month and year from the 'date' column
    df['month_year'] = df['date'].dt.to_period('M')
    
    # Convert 'month_year' column to string
    df['month_year'] = df['month_year'].astype(str)

    # Group by month and calculate the total expenditure for each month
    monthly_expense = df.groupby('month_year')['total_amount'].sum().reset_index()
    
    return monthly_expense

def expenditure_and_percentage_change(pool, username):
    current_date = datetime.now()
    latest_month_to_check = current_date.month
    previous_month_to_check = latest_month_to_check - 1

    query = sqlalchemy.text("""
        SELECT date, total_amount
        FROM receipt_details_2
        WHERE username = :username
    """)

    result = pool.execute(query, {"username": username}).fetchall()

    expenditure = {latest_month_to_check: 0,
                   previous_month_to_check: 0}

    for row in result:
        year = int(row['date'].split("-")[0])
        month = int(row['date'].split("-")[1])

        if month == latest_month_to_check:
            expenditure[latest_month_to_check] += float(row['total_amount'])
        elif month == previous_month_to_check:
            expenditure[previous_month_to_check] += float(row['total_amount'])
            
    print(f"expenditure = {expenditure}")
            
    percentage_change = ((expenditure[previous_month_to_check] - expenditure[latest_month_to_check]) / (expenditure[previous_month_to_check] + expenditure[latest_month_to_check])) * 100
    
    print(f"expenditure[previous_month_to_check] = {expenditure[previous_month_to_check]}, expenditure[latest_month_to_check] = {expenditure[latest_month_to_check]}")
    
    if percentage_change < 0:
        result = str(abs(round(percentage_change, 2))) + '+'
    else:
        result = str(abs(round(percentage_change, 2))) + '-'
            
    return result

def analytics(pool, username):
    
    total_expenditure = calculate_total_expenditure_latest_month(pool, username)
    cat_expenditure = calculate_category_wise_expenditure_latest_month(pool, username)
    transaction_details = get_latest_transaction_details(pool, username)
    highest_spending_category = calculate_highest_spending_category_latest_month(pool, username)
    monthly_expense = monthly_expenditure_trends(pool, username)
    percentage_change = expenditure_and_percentage_change(pool, username)
    
    return total_expenditure, cat_expenditure, transaction_details, highest_spending_category, monthly_expense, percentage_change

