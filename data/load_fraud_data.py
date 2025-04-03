from neo4j import GraphDatabase
import os
from dotenv import load_dotenv
import random
from datetime import datetime, timedelta
import uuid

# Load environment variables
load_dotenv()

class FraudDataLoader:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI"),
            auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
        )

    def close(self):
        self.driver.close()

    def create_constraints(self):
        with self.driver.session() as session:
            # Create constraints for unique properties
            session.run("CREATE CONSTRAINT account_id IF NOT EXISTS FOR (a:Account) REQUIRE a.account_id IS UNIQUE")
            session.run("CREATE CONSTRAINT transaction_id IF NOT EXISTS FOR (t:Transaction) REQUIRE t.transaction_id IS UNIQUE")
            session.run("CREATE CONSTRAINT device_id IF NOT EXISTS FOR (d:Device) REQUIRE d.device_id IS UNIQUE")
            session.run("CREATE CONSTRAINT ip_address IF NOT EXISTS FOR (i:IPAddress) REQUIRE i.ip IS UNIQUE")

    def generate_test_data(self):
        # Generate accounts
        accounts = []
        for i in range(100):
            account = {
                "account_id": f"ACC_{uuid.uuid4().hex[:8]}",
                "type": random.choice(["personal", "business"]),
                "status": random.choice(["active", "suspended", "closed"]),
                "risk_score": random.randint(0, 100),
                "created_at": (datetime.now() - timedelta(days=random.randint(0, 365))).isoformat()
            }
            accounts.append(account)

        # Generate devices
        devices = []
        for i in range(50):
            device = {
                "device_id": f"DEV_{uuid.uuid4().hex[:8]}",
                "type": random.choice(["mobile", "desktop", "tablet"]),
                "os": random.choice(["iOS", "Android", "Windows", "macOS"]),
                "fingerprint": uuid.uuid4().hex
            }
            devices.append(device)

        # Generate IP addresses
        ip_addresses = []
        for i in range(30):
            ip = {
                "ip": f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}",
                "country": random.choice(["US", "UK", "CA", "AU", "IN", "BR", "DE", "FR"]),
                "is_vpn": random.choice([True, False])
            }
            ip_addresses.append(ip)

        # Generate transactions
        transactions = []
        for i in range(200):
            transaction = {
                "transaction_id": f"TXN_{uuid.uuid4().hex[:8]}",
                "amount": round(random.uniform(10, 10000), 2),
                "currency": random.choice(["USD", "EUR", "GBP", "CAD"]),
                "type": random.choice(["purchase", "transfer", "withdrawal", "deposit"]),
                "status": random.choice(["completed", "failed", "pending"]),
                "timestamp": (datetime.now() - timedelta(hours=random.randint(0, 24))).isoformat(),
                "is_fraudulent": random.choice([True, False])
            }
            transactions.append(transaction)

        return accounts, devices, ip_addresses, transactions

    def load_data(self):
        accounts, devices, ip_addresses, transactions = self.generate_test_data()

        with self.driver.session() as session:
            # Create accounts
            for account in accounts:
                session.run("""
                    CREATE (a:Account {
                        account_id: $account_id,
                        type: $type,
                        status: $status,
                        risk_score: $risk_score,
                        created_at: $created_at
                    })
                """, account)

            # Create devices
            for device in devices:
                session.run("""
                    CREATE (d:Device {
                        device_id: $device_id,
                        type: $type,
                        os: $os,
                        fingerprint: $fingerprint
                    })
                """, device)

            # Create IP addresses
            for ip in ip_addresses:
                session.run("""
                    CREATE (i:IPAddress {
                        ip: $ip,
                        country: $country,
                        is_vpn: $is_vpn
                    })
                """, ip)

            # Create transactions and relationships
            for transaction in transactions:
                # Create transaction
                session.run("""
                    CREATE (t:Transaction {
                        transaction_id: $transaction_id,
                        amount: $amount,
                        currency: $currency,
                        type: $type,
                        status: $status,
                        timestamp: $timestamp,
                        is_fraudulent: $is_fraudulent
                    })
                """, transaction)

                # Create relationships
                # Connect transaction to random account
                account = random.choice(accounts)
                session.run("""
                    MATCH (a:Account {account_id: $account_id})
                    MATCH (t:Transaction {transaction_id: $transaction_id})
                    CREATE (a)-[:PERFORMED]->(t)
                """, {
                    "account_id": account["account_id"],
                    "transaction_id": transaction["transaction_id"]
                })

                # Connect transaction to random device
                device = random.choice(devices)
                session.run("""
                    MATCH (d:Device {device_id: $device_id})
                    MATCH (t:Transaction {transaction_id: $transaction_id})
                    CREATE (d)-[:USED_FOR]->(t)
                """, {
                    "device_id": device["device_id"],
                    "transaction_id": transaction["transaction_id"]
                })

                # Connect transaction to random IP
                ip = random.choice(ip_addresses)
                session.run("""
                    MATCH (i:IPAddress {ip: $ip})
                    MATCH (t:Transaction {transaction_id: $transaction_id})
                    CREATE (i)-[:ORIGINATED_FROM]->(t)
                """, {
                    "ip": ip["ip"],
                    "transaction_id": transaction["transaction_id"]
                })

                # Create suspicious patterns
                if transaction["is_fraudulent"]:
                    # Create suspicious pattern node
                    pattern_id = f"PAT_{uuid.uuid4().hex[:8]}"
                    session.run("""
                        CREATE (p:SuspiciousPattern {
                            pattern_id: $pattern_id,
                            type: $type,
                            severity: $severity,
                            description: $description
                        })
                        WITH p
                        MATCH (t:Transaction {transaction_id: $transaction_id})
                        CREATE (t)-[:EXHIBITS]->(p)
                    """, {
                        "pattern_id": pattern_id,
                        "type": random.choice(["velocity", "geolocation", "device_anomaly", "ip_anomaly"]),
                        "severity": random.choice(["high", "medium", "low"]),
                        "description": "Suspicious transaction pattern detected",
                        "transaction_id": transaction["transaction_id"]
                    })

    def create_indexes(self):
        with self.driver.session() as session:
            # Create indexes for better query performance
            session.run("CREATE INDEX account_risk_score IF NOT EXISTS FOR (a:Account) ON (a.risk_score)")
            session.run("CREATE INDEX transaction_timestamp IF NOT EXISTS FOR (t:Transaction) ON (t.timestamp)")
            session.run("CREATE INDEX transaction_amount IF NOT EXISTS FOR (t:Transaction) ON (t.amount)")
            session.run("CREATE INDEX pattern_type IF NOT EXISTS FOR (p:SuspiciousPattern) ON (p.type)")

if __name__ == "__main__":
    loader = FraudDataLoader()
    try:
        print("Creating constraints...")
        loader.create_constraints()
        
        print("Creating indexes...")
        loader.create_indexes()
        
        print("Loading test data...")
        loader.load_data()
        
        print("Test data loaded successfully!")
    finally:
        loader.close() 