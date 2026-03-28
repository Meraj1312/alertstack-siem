#  Phase 1 — Risk Scoring Engine

##  Objective

The goal of Phase 1 was to design and implement a **policy-driven, event-level risk scoring engine** for the FinTech Mini-SIEM system.

This phase transforms raw normalized events into **enriched security events** by assigning:

* Risk scores
* Severity levels
* Detection flags

The system is designed to mimic real-world SIEM behavior while maintaining **clean architecture and extensibility**.

---

##  Architecture Overview

###  Processing Pipeline

```
Raw Event
   ↓
Validation (Pydantic)
   ↓
Normalization
   ↓
Risk Engine (Phase 1)
   ↓
Enriched Event
   ↓
Event Store
```

---

##  Core Components

### 1️ Policy Manager (`config.py`)

Responsible for:

* Loading policy from JSON
* Validating schema and logic
* Maintaining active policy version

#### Key Features

* Mandatory field validation
* Rule uniqueness enforcement (`rule_id`)
* Risk score boundary validation
* Severity range validation (no overlaps)
* Fail-safe policy activation (invalid policy rejected)

---

### 2️ Policy File (`policy.json`)

Fully **config-driven system**.

#### Structure

```json
{
  "policy_version": "1.0.0",
  "global_settings": {
    "default_risk_score": 0,
    "max_risk_score": 100
  },
  "severity_levels": [...],
  "rules": [...]
}
```

#### Capabilities

* Dynamic severity mapping
* Configurable rules
* Threshold-based conditions
* Extensible for future rule types

---

### 3️ Rule Engine (`rules.py`)

Stateless rule evaluation module.

#### Design Principles

* Pure function (`evaluate_rule`)
* No memory/state
* Deterministic behavior
* Easy to extend

#### Supported Conditions

* `event_type`
* `amount_gt` (threshold-based condition)

---

### 4️ Risk Engine (`engine.py`)

Core computation engine.

#### Responsibilities

* Apply all enabled rules
* Aggregate risk scores
* Enforce max risk cap
* Resolve severity dynamically
* Attach risk metadata to event

#### Risk Object Structure

```json
{
  "score": 70,
  "severity": "high",
  "flags": ["RULE_ID"],
  "calculated_at": "timestamp",
  "policy_version": "1.0.0"
}
```

---

##  Design Decisions

| Component        | Decision                                |
| ---------------- | --------------------------------------- |
| Policy Storage   | JSON file (DB planned in future phases) |
| Rule Execution   | Stateless, config-driven                |
| Severity         | Fully policy-defined                    |
| Risk Aggregation | Additive with upper cap                 |
| Engine Failure   | Fail-open (no ingestion blocking)       |
| API Response     | Success acknowledgment (risk optional)  |

---

##  Fail-Open Behavior

If the Risk Engine fails:

* Event ingestion continues
* Risk is set to:

```json
{
  "score": null,
  "severity": null,
  "flags": [],
  "calculated_at": null
}
```

This ensures:

✔ No data loss
✔ System resilience
✔ Continuous ingestion

---

##  Testing Strategy

###  Functional Tests

| Test Case              | Expected Outcome         |
| ---------------------- | ------------------------ |
| Failed login           | score = 20               |
| High value transaction | score = 70               |
| No match               | score = 0                |
| Multiple rules         | aggregated score         |
| Score overflow         | capped at max_risk_score |

---

### ✅ System Tests

| Test                 | Result                    |
| -------------------- | ------------------------- |
| Duplicate event_id   | Rejected (406)            |
| Invalid policy       | Startup failure           |
| Fail-open simulation | Risk = null, event stored |
| Severity mapping     | Dynamic from policy       |

---

##  Example Output

```json
{
  "event_id": "101",
  "event_type": "login_failed",
  "risk": {
    "score": 20,
    "severity": "low",
    "flags": ["FAILED_LOGIN"],
    "policy_version": "1.0.0"
  }
}
```

---

##  Project Structure (Phase 1)

```
app/
├── api/
│   └── ingestion.py
├── core/
│   ├── event_store.py
│   └── normalization.py
├── risk/
│   ├── config.py
│   ├── engine.py
│   ├── policy.json
│   └── rules.py
├── schemas/
│   └── event_schema.py
└── main.py
```

---

##  Key Achievements

* Built a **policy-driven risk engine**
* Implemented **clean architecture separation**
* Designed **extensible rule framework**
* Ensured **fail-safe ingestion pipeline**
* Achieved **full test coverage for Phase 1 scenarios**

---

##  Next Phase

### Phase 2 — Behavioral Correlation

Upcoming capabilities:

* Multi-event correlation
* Time-window analysis
* Brute-force detection
* User behavior tracking
* Context-aware risk amplification

---

##  Summary

Phase 1 successfully transforms the system from:

> Passive event collector → Intelligent risk-aware SIEM pipeline

This lays the foundation for advanced detection and correlation in upcoming phases.
