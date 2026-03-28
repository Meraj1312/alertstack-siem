#  AlertStack — Phase 4: SOC Visibility Layer

##  Overview

Phase 4 transforms **AlertStack** from a backend detection pipeline into a **SOC-usable system**.

Until Phase 3, the system focused on:

* ingesting events
* scoring risk
* correlating behaviors
* generating detections

Phase 4 introduces the **analyst-facing layer**, enabling:

* investigation workflows
* alert triage
* system monitoring
* incident reporting

This phase simulates how real-world SIEM platforms expose data to security analysts.

---

##  Architecture Extension

### Previous Pipeline

```
Raw → Normalize → Risk → Correlation → Detection → Storage
```

### Phase 4 Addition

```
Storage → Query Layer → SOC APIs → Reporting
```

---

##  New Components Added

```
app/
├── api/
│   ├── events.py
│   ├── alerts.py
│   ├── users.py
│   ├── metrics.py
│   └── reports.py
│
├── core/
│   ├── event_store.py (updated)
│   ├── query_engine.py (or query logic added)
│   └── alert_builder.py
│
├── schemas/
│   ├── event_response.py
│   └── alert_response.py
│
├── reporting/
│   └── exporter.py
```

---

##  1. Events API — Log Search Layer

### Endpoint

```
GET /events
```

### Features

* Filter by:

  * `user_id`
  * `event_type`
  * `severity` (risk-based)
  * `start_time`, `end_time`
* Pagination (`limit`, `offset`)
* Sorted by newest first

### Purpose

Acts as a **search interface over enriched events**, similar to querying logs in a SIEM.

---

##  2. Alerts API — SOC Alert Feed

### Endpoint

```
GET /alerts
```

### Features

* Extracts alerts from detection layer
* Filters:

  * `user_id`
  * `severity` (detection-based)
  * time range
* Pagination support

### Alert Structure

```json
{
  "alert_id": "evt-123::ATO",
  "timestamp": "...",
  "user_id": "U123",
  "type": "account_takeover",
  "severity": "critical",
  "confidence": 0.92,
  "reason": "...",
  "mitre": ["T1110"],
  "event_id": "evt-123"
}
```

### Purpose

Provides a **high-signal feed for analysts**, similar to real SOC alert dashboards.

---

##  3. User Activity API — Investigation Timeline

### Endpoint

```
GET /users/{user_id}/activity
```

### Features

* Returns full event timeline for a user
* Includes:

  * risk
  * correlation
  * detection
* Sorted **oldest → newest**

### Purpose

Supports **incident investigation workflows**, enabling analysts to trace attack sequences.

---

##  4. Metrics API — SOC Overview

### Endpoint

```
GET /metrics
```

### Features

* Total events
* Total alerts
* High severity alert count
* Severity distribution
* Event type breakdown
* Time filtering

### Purpose

Provides **system-level visibility**, similar to SIEM dashboards.

---

##  5. Report Export — Incident Reporting

### Endpoint

```
GET /reports/alerts
```

### Features

* Export alerts in:

  * JSON (default)
  * Markdown (`?format=markdown`)
* Supports filtering (user, severity, time)

### Markdown Output Includes

* summary section
* alert breakdown
* reason
* MITRE mapping
* timestamps

### Purpose

Generates **analyst-ready incident reports** for documentation and sharing.

---

##  Key Engineering Concepts Introduced

### 1. Query Layer

* Centralized filtering logic (`query_events`)
* Prevents duplication across APIs

---

### 2. Alert Transformation Layer

* Converts detection output → structured alerts
* Decouples detection from presentation

---

### 3. Separation of Concerns

| Layer       | Responsibility        |
| ----------- | --------------------- |
| ingestion   | data entry            |
| risk        | scoring               |
| correlation | behavior linking      |
| detection   | threat identification |
| storage     | persistence           |
| query       | filtering             |
| API         | exposure              |
| reporting   | output formatting     |

---

### 4. SOC Workflow Simulation

Phase 4 enables a realistic workflow:

1. Alerts API → identify suspicious activity
2. User Activity API → investigate user behavior
3. Events API → deep search
4. Metrics API → monitor system
5. Reports API → document incident

---

##  Design Decisions

### No Separate Alert Storage

Alerts are derived dynamically from events:

* avoids duplication
* keeps system simple
* mirrors lightweight SIEM design

---

### In-Memory Querying

* acceptable for prototype
* sets foundation for DB-backed querying in Phase 5

---

##  Outcome

After Phase 4, AlertStack supports:

* ✅ Event search
* ✅ Alert triage
* ✅ User investigation
* ✅ System monitoring
* ✅ Incident reporting

---

##  System Maturity Upgrade

| Capability     | Before | After |
| -------------- | ------ | ----- |
| Detection      | ✅      | ✅     |
| Correlation    | ✅      | ✅     |
| SOC Visibility | ❌      | ✅     |
| Investigation  | ❌      | ✅     |
| Reporting      | ❌      | ✅     |

---

##  Conclusion

Phase 4 completes the transition from:

> “Detection pipeline”

to:

> **“SOC-oriented SIEM backend”**

This phase is critical in demonstrating:

* practical security engineering skills
* understanding of analyst workflows
* ability to design usable security systems

---

##  Next Phase

### Phase 5 — Production & Realism

Focus areas:

* persistent storage (database)
* performance improvements
* indexing and optimization
* real-world readiness

---
