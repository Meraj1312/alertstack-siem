# Phase 3 — FinTech Security & Threat Detection

## Objective

Enhance the SIEM pipeline with security-focused detection logic to simulate real-world FinTech threat scenarios such as:

* Account Takeover (ATO)
* Fraudulent Transactions
* Geo-based anomalies
* Multi-event attack patterns

This phase introduces a Detection Engine that operates after correlation and enriches events with analyst-facing alerts.

---

## Architecture Overview

### Updated Pipeline

```
Raw Event
→ Validation
→ Normalization
→ Risk Engine
→ Correlation Engine
→ Detection Engine
→ Enriched Event → Storage
```

---

## Detection Layer Design

A new modular layer was introduced:

```
detection/
├── engine.py
├── context.py
└── rules/
    ├── ato.py
    ├── fraud.py
    ├── geo.py
    └── sequence.py
```

---

## Core Components

### 1. DetectionEngine

* Executes detection rules
* Aggregates alerts
* Computes severity and confidence
* Handles cross-event escalation (ATO + Fraud)

---

### 2. DetectionContext

Maintains state required for behavioral detection:

* Login history (for ATO detection)
* Transaction history (for fraud detection)
* User transaction baseline (average amount)
* Last known IP and location
* ATO state tracking (time-based)

---

## Detection Rules Implemented

---

### 1. Account Takeover (ATO)

Detects:
Multiple failed login attempts followed by a successful login.

Logic:

* Tracks login attempts within a 5-minute window
* If 5 or more failures are followed by a success, an alert is triggered

Output Example:

```json
{
  "type": "ATO",
  "severity": "high",
  "confidence": 85,
  "reason": "5 failed logins followed by success",
  "mitre": "T1110"
}
```

---

### 2. Fraud Detection

#### a) Transaction Velocity

Detects:
High number of transactions in a short time window.

* 5 or more transactions within 5 minutes

---

#### b) Transaction Anomaly (Baseline-Based)

Detects:
Deviation from a user’s normal transaction behavior.

Logic:

* Maintain average transaction amount per user
* Flag if current transaction exceeds three times the average

Output Example:

```json
{
  "type": "FRAUD_ANOMALY",
  "severity": "high",
  "confidence": 85,
  "reason": "Transaction 5000 vs user avg 500",
  "mitre": "T1499"
}
```

---

### 3. Geo Anomaly (Impossible Travel)

Detects:
Logins from different geographic locations within a short time.

Logic:

* Map IP to location (mocked dataset)
* Compare with previous login location

Output Example:

```json
{
  "type": "IMPOSSIBLE_TRAVEL",
  "severity": "high",
  "confidence": 90,
  "reason": "Login from IN to US",
  "mitre": "T1078"
}
```

---

### 4. Suspicious Sequence

Detects:
A login followed by a transaction within a short time window.

---

## Cross-Event Detection

### ATO + Transaction Escalation

Detects:
A transaction occurring shortly after a suspected account takeover.

Logic:

* If ATO is detected within the last 10 minutes
* And a transaction occurs
* Trigger a critical alert

Output Example:

```json
{
  "type": "ATO_FRAUD_COMBO",
  "severity": "critical",
  "confidence": 95,
  "reason": "Transaction within 10 minutes of suspected account takeover",
  "mitre": "T1078"
}
```

---

## Detection Output Structure

Each event is enriched with:

```json
"detection": {
  "alerts": [],
  "flags": [],
  "severity": "low | medium | high | critical",
  "confidence": 0-100
}
```

---

## Design Principles

* Modular rule-based architecture
* Context-aware detection (stateful processing)
* Explainable alerts with clear reasoning
* Fail-open behavior (detection failure does not block ingestion)
* Self-contained implementation (no external dependencies)

---

## Limitations

* Static thresholds (no adaptive tuning)
* No device fingerprinting
* IP-to-location mapping is mocked
* Vulnerable to low-and-slow attack patterns
* No long-term behavioral profiling

---

## Outcome

Phase 3 transforms the system from an event processing pipeline into a security detection engine.

The system now supports:

* Behavioral analysis
* Multi-event correlation
* Analyst-ready alert generation

---

## Next Phase

Phase 4 — SOC Visibility Layer

* Alerts API
* Event querying
* Analyst-facing views
* Reporting capabilities
