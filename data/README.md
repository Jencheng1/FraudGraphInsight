# Fraud Graph Test Data

This directory contains scripts and documentation for generating test data for the FraudGraphInsight system.

## Data Structure

The test data represents a fraud detection graph with the following node types and relationships:

### Node Types

1. **Account**
   - Properties:
     - `account_id` (unique identifier)
     - `type` (personal/business)
     - `status` (active/suspended/closed)
     - `risk_score` (0-100)
     - `created_at` (timestamp)

2. **Transaction**
   - Properties:
     - `transaction_id` (unique identifier)
     - `amount` (decimal)
     - `currency` (USD/EUR/GBP/CAD)
     - `type` (purchase/transfer/withdrawal/deposit)
     - `status` (completed/failed/pending)
     - `timestamp` (ISO format)
     - `is_fraudulent` (boolean)

3. **Device**
   - Properties:
     - `device_id` (unique identifier)
     - `type` (mobile/desktop/tablet)
     - `os` (iOS/Android/Windows/macOS)
     - `fingerprint` (unique device identifier)

4. **IPAddress**
   - Properties:
     - `ip` (unique IP address)
     - `country` (country code)
     - `is_vpn` (boolean)

5. **SuspiciousPattern**
   - Properties:
     - `pattern_id` (unique identifier)
     - `type` (velocity/geolocation/device_anomaly/ip_anomaly)
     - `severity` (high/medium/low)
     - `description` (text)

### Relationships

1. `(Account)-[:PERFORMED]->(Transaction)`
   - Represents an account performing a transaction

2. `(Device)-[:USED_FOR]->(Transaction)`
   - Represents the device used for a transaction

3. `(IPAddress)-[:ORIGINATED_FROM]->(Transaction)`
   - Represents the IP address from which a transaction originated

4. `(Transaction)-[:EXHIBITS]->(SuspiciousPattern)`
   - Represents suspicious patterns detected in a transaction

## Data Generation

The test data is generated with the following characteristics:

- 100 accounts (mix of personal and business)
- 50 devices (mix of mobile, desktop, and tablet)
- 30 IP addresses (mix of VPN and non-VPN)
- 200 transactions (mix of legitimate and fraudulent)
- Random relationships between entities
- Suspicious patterns for fraudulent transactions

## Usage

To generate and load the test data:

1. Ensure Neo4j is running and accessible
2. Set up environment variables in `.env`:
   ```
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=your_password
   ```
3. Run the data loader:
   ```bash
   python load_fraud_data.py
   ```

## Example Queries

Here are some example Cypher queries you can use to explore the data:

1. Find high-risk accounts with fraudulent transactions:
   ```cypher
   MATCH (a:Account)-[:PERFORMED]->(t:Transaction)-[:EXHIBITS]->(p:SuspiciousPattern)
   WHERE a.risk_score > 80 AND p.severity = 'high'
   RETURN a, t, p
   ```

2. Find transactions from VPN IPs:
   ```cypher
   MATCH (i:IPAddress)-[:ORIGINATED_FROM]->(t:Transaction)
   WHERE i.is_vpn = true
   RETURN i, t
   ```

3. Find device anomalies:
   ```cypher
   MATCH (d:Device)-[:USED_FOR]->(t:Transaction)-[:EXHIBITS]->(p:SuspiciousPattern)
   WHERE p.type = 'device_anomaly'
   RETURN d, t, p
   ``` 