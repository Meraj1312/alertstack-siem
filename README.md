#  AlertStack — FinTech Mini-SIEM (SOC-Focused)

AlertStack is a **Security Information and Event Management (SIEM) backend system** designed to simulate real-world **FinTech threat detection pipelines**.

It processes events through a full detection lifecycle and exposes APIs for **SOC investigation workflows**.

---

##  Project Goal

To build a **practical, detection-focused SIEM system** that demonstrates:

* event ingestion & normalization
* risk scoring
* correlation & behavioral analysis
* detection engineering
* SOC visibility (alerts, timelines, metrics)

---

##  Architecture

```
Raw Event
   ↓
Normalization
   ↓
Risk Engine
   ↓
Correlation Engine
   ↓
Detection Engine
   ↓
SQLite Storage
   ↓
APIs (Events / Alerts / Metrics / Users / Reports)
```

---

##  Key Features

###  Event Processing Pipeline

* Structured ingestion using FastAPI
* Schema validation with Pydantic
* Normalized event format

---

###  Risk Scoring Engine

* Policy-driven scoring (`policy.json`)
* Outputs:

  * score
  * severity
  * flags

---

###  Correlation Engine

* Sliding window detection
* Multi-event tracking:

  * brute force attempts
  * transaction spikes
* Alert suppression logic

---

###  Detection Engine

Implements real-world detection scenarios:

* Account Takeover (ATO)
* Fraud detection:

  * velocity-based
  * behavioral deviation
* Geo anomaly (impossible travel)
* Sequence-based attacks

Each detection produces:

```
alerts, severity, confidence, reason
```

---

###  SOC Visibility APIs

#### Events API

```
GET /events
```

* filtering (user, type, severity, time)
* pagination

---

#### Alerts API

```
GET /alerts
```

* SOC-style alert feed
* includes severity, confidence, MITRE mapping

---

#### User Activity API

```
GET /users/{user_id}/activity
```

* investigation timeline (old → new)

---

#### Metrics API

```
GET /metrics
```

* total events
* total alerts
* severity distribution
* event type breakdown

---

#### Report Export

```
GET /reports/alerts
```

* JSON + Markdown incident reports

---

##  Storage

* SQLite database
* JSON-serialized event storage
* Stores:

  * raw event
  * normalized event
  * risk output
  * correlation output
  * detection output

---

##  Testing

* Unit Tests:

  * risk engine
  * detection rules
  * correlation logic

* Integration Tests:

  * full pipeline validation (ingest → detect → store → query)

Run tests:

```
pytest -v
```

---

##  Setup

```bash
git clone <repo>
cd AlertStack

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

##  Example Event

```json
{
  "event_id": "evt-123",
  "event_type": "login",
  "timestamp": "2026-01-01T10:00:00",
  "source_ip": "1.1.1.1",
  "outcome": "success",
  "user_id": "user-1",
  "event_data": {
    "device": "chrome"
  },
  "context": {
    "location": "IN"
  }
}
```

---

##  What This Demonstrates

This project shows:

* backend system design (FastAPI + SQLite)
* detection engineering mindset
* stateful correlation logic
* real-world debugging (time handling, serialization, DB)
* test-driven development

---

##  Future Improvements

* PostgreSQL support
* async DB layer
* rule engine externalization
* Docker deployment
* real-time streaming (Kafka)

---


Built as part of a hands-on journey toward becoming a **Security Engineer / Penetration Tester**.
