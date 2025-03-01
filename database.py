import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Table, Column, String, Integer, Float, Date, MetaData, select

# Database Configuration
DB_USER = "root"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "customer"

# Create MySQL Connection
engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
metadata = MetaData()

# Define Transactions Table
transactions = Table(
    "transactions", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sender", String(50)),
    Column("receiver", String(50)),
    Column("amount", Float),
    Column("date", Date),
)

# Create the table in MySQL if not exists
metadata.create_all(engine)

# Generate Sample Data
random.seed(42)
account_numbers = [f"AC{1000 + i}" for i in range(20)]  # 20 unique accounts


def generate_sample_transactions():
    data = []
    today = datetime.today()

    # **Fraud Ring Transactions (Circular Transactions)**
    fraud_ring = ["AC1001", "AC1002", "AC1003", "AC1004"]
    for i in range(len(fraud_ring)):
        sender = fraud_ring[i]
        receiver = fraud_ring[(i + 1) % len(fraud_ring)]  # Circular transfer
        data.append({
            "sender": sender,
            "receiver": receiver,
            "amount": random.randint(5000, 20000),
            "date": today - timedelta(days=random.randint(1, 30))
        })

    # **Mule Accounts (High-Value Transfers, Then Disbursement)**
    mule_account = "AC1010"
    for i in range(3):
        sender = f"AC10{5 + i}"
        data.append({
            "sender": sender,
            "receiver": mule_account,
            "amount": random.randint(20000, 50000),
            "date": today - timedelta(days=random.randint(1, 30))
        })
    for i in range(3):
        receiver = f"AC10{8 + i}"
        data.append({
            "sender": mule_account,
            "receiver": receiver,
            "amount": random.randint(5000, 10000),
            "date": today - timedelta(days=random.randint(1, 30))
        })

    # **Legitimate Transactions (Normal Transfers)**
    for _ in range(40):
        sender, receiver = random.sample(account_numbers, 2)
        data.append({
            "sender": sender,
            "receiver": receiver,
            "amount": random.randint(100, 4000),
            "date": today - timedelta(days=random.randint(1, 30))
        })

    return data

# # Insert Sample Data
# sample_transactions = generate_sample_transactions()

# with engine.connect() as conn:
#     conn.execute(transactions.insert(), sample_transactions)
#     conn.commit()  # Commit transaction

# print("✅ Sample data inserted successfully!")


def fetch_transactions():
    """Fetch transaction data from MySQL database."""
    with engine.connect() as conn:
        metadata.create_all(engine)  # Ensure table exists
        stmt = select(transactions)  # Explicit query statement
        print("Fetching transactions from database...")
        result = conn.execute(stmt).fetchall()
        print(f"Fetched {len(result)} transactions.")

    return [
        {
            "sender": row.sender,
            "receiver": row.receiver,
            "amount": row.amount,
            "date": datetime.strptime(str(row.date), "%Y-%m-%d")  # Convert to datetime object
        }
        for row in result
    ]
