#  Phase 2 — Behavioral Correlation & Multi-Event Intelligence

##  Overview

Phase 2 introduces **stateful behavioral correlation** into the SIEM pipeline.

Unlike Phase 1 (which evaluates events in isolation), this phase enables the system to:

* Analyze **event sequences over time**
* Detect **behavioral patterns**
* Correlate **multiple events for a single entity (user)**
* Generate **context-aware detections**

This transforms the system from a rule-based scorer into a **detection engine with SOC-like capabilities**.

---

##  Architecture Integration

### Updated Pipeline

```
Raw Event
→ Validation
→ Normalization
→ Risk Engine
→ Correlation Engine
→ Enriched Event (risk + correlation)
→ Event Store
```

---

##  Core Concepts Implemented

### 1️ Stateful Correlation

* Introduced **StateManager**
* Maintains access to historical events
* Enables querying based on:

  * `user_id`
  * `event_type`
  * `time window`

Supports:

* Sliding window analysis
* Temporal event grouping

---

### 2️ Sliding Window Logic

* Time-based filtering of events
* Example:

  * Last 5 minutes (300 seconds)
  * Last 2 minutes (120 seconds)

Used for:

* Brute force detection
* Transaction spike detection

---

### 3️ Multi-Rule Detection Engine

* Introduced **RULES list**
* Detection rules are:

  * Modular
  * Independent
  * Extensible

```python
RULES = [
    detect_bruteforce,
    detect_transaction_spike
]
```

* Engine iterates over rules dynamically
* Enables plug-and-play detection design

---

### 4️ Behavioral Detection Rules

####  Brute Force Detection

Detects repeated failed login attempts.

* Event Type: `login_failed`
* Window: 300 seconds
* Escalation thresholds:

  * ≥5 → MEDIUM
  * ≥10 → HIGH
  * ≥20 → CRITICAL

---

####  Transaction Spike Detection

Detects rapid transaction bursts.

* Event Type: `transaction`
* Window: 120 seconds
* Threshold:

  * ≥5 transactions → alert

---

### 5️ Escalation Logic

Introduced **progressive severity based on behavior intensity**.

Example (Brute Force):

| Attempts | Severity | Score |
| -------- | -------- | ----- |
| 5–9      | Medium   | 40    |
| 10–19    | High     | 70    |
| 20+      | Critical | 90    |

Enables:

* Context-aware severity
* Reduced false positives
* Analyst prioritization

---

### 6️ Alert Suppression (Deduplication)

Implemented via **AlertState**.

Prevents alert flooding by:

* Tracking recent alerts per:

  * `user_id`
  * `rule_id`
* Suppressing duplicate alerts within a time window

Example:

* 5th login failure → alert
* 6th login failure → suppressed

---

### 7️ Context Enrichment

Each detection includes **behavioral metadata**:

Examples:

```json
{
  "attempt_count": 10,
  "window_seconds": 300
}
```

```json
{
  "transaction_count": 5,
  "window_seconds": 120
}
```

Improves:

* Analyst visibility
* Debugging
* Detection explainability

---

### 8️ MITRE ATT&CK Mapping

Each rule maps to relevant techniques:

| Detection         | Technique ID | Name                     |
| ----------------- | ------------ | ------------------------ |
| Brute Force       | T1110        | Brute Force              |
| Transaction Spike | T1499        | Endpoint DoS (Simulated) |

Adds:

* Threat context
* Industry alignment
* Detection classification

---

### 9️ Fail-Open Design

* Correlation failures do **not block ingestion**
* System continues processing events

```json
"correlation": null
```

Ensures:

* No data loss
* High availability

---

##  Output Structure

Each enriched event now includes:

```json
{
  "risk": { ... },
  "correlation": {
    "behavioral_score": 60,
    "flags": ["TRANSACTION_SPIKE"],
    "matched_rules": ["TRANSACTION_SPIKE"],
    "mitre": [...],
    "context": [...],
    "evaluated_at": "timestamp"
  }
}
```

---

##  Testing & Validation

Validated scenarios:

* ✅ Brute force detection (5, 10, 20 attempts)
* ✅ Escalation logic (medium → high → critical)
* ✅ Alert suppression (duplicate prevention)
* ✅ Cooldown-based re-trigger
* ✅ Transaction spike detection
* ✅ Multi-rule execution
* ✅ MITRE mapping correctness
* ✅ Context enrichment accuracy
* ✅ Fail-open behavior

---

##  Key Engineering Learnings

* Detection requires **state**, not just rules
* Time-based correlation is essential for SOC systems
* Alert suppression is critical for noise reduction
* Escalation improves signal quality
* Context makes detections actionable
* Modular design enables scalability

---

##  Outcome

Phase 2 transforms the system into a:

> **Behavioral Detection Engine**

Capabilities now include:

* Multi-event correlation
* Temporal analysis
* Stateful tracking
* Multi-rule detection
* Alert lifecycle (partial)
* Threat mapping (MITRE)

---

##  Phase Status

```
Phase 2 — 100% Complete
```

---

##  Next Phase

### Phase 3 — FinTech Security & Threat Detection

Focus:

* Account Takeover (ATO)
* Fraud detection patterns
* Behavioral anomalies
* Geo-based detection

---
