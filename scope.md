# SCOPING
## **Data Contract (Critical Fields)**
Below is a minimal JSON Schema describing **5–7 most critical fields** from the Companies House **Company Profile** resource for supplier risk analysis.

These fields focus on:
- Legal existence
- Operational status
- Financial recency
- Legal exposure
- Corporate traceability


### Rationale for Field Selection

| Field | Why it matters for supplier risk |
|------|--------------------------------|
| `company_number` | Unique legal identifier |
| `company_name` | Legal entity verification |
| `company_status` | Determines if company is active, dissolved, liquidated, etc |
| `date_of_creation` | Company age & operational maturity |
| `date_of_cessation` | Indicates termination |
| `accounts.last_accounts.made_up_to` | Financial reporting freshness |
| `has_charges` | Indicates outstanding secured debt |


### JSON Schema

```json
{
  "title": "Supplier Risk Company Profile",
  "type": "object",
  "required": [
    "company_number",
    "company_name",
    "company_status",
    "date_of_creation",
    "accounts",
    "has_charges"
  ],
  "properties": {
    "company_number": {
      "type": "string",
      "description": "Unique Companies House identifier"
    },
    "company_name": {
      "type": "string",
      "description": "Registered legal name of the company"
    },
    "company_status": {
      "type": "string",
      "enum": [
        "active",
        "dissolved",
        "liquidation",
        "administration",
        "receivership"
      ],
      "description": "Current legal status of the company"
    },
    "date_of_creation": {
      "type": "string",
      "format": "date",
      "description": "Date the company was incorporated"
    },
    "date_of_cessation": {
      "type": ["string", "null"],
      "format": "date",
      "description": "Date the company was dissolved or ceased trading"
    },
    "accounts": {
      "type": "object",
      "required": ["last_accounts"],
      "properties": {
        "last_accounts": {
          "type": "object",
          "required": ["made_up_to", "type"],
          "properties": {
            "made_up_to": {
              "type": "string",
              "format": "date",
              "description": "Last available financial reporting period"
            },
            "type": {
              "type": "string",
              "description": "Type of financial statement"
            }
          }
        }
      }
    },
    "has_charges": {
      "type": "boolean",
      "description": "Indicates whether the company has registered secured charges"
    }
  }
}
```
---
## Pagination Risks
When an API uses start_index (offset-based pagination), new companies created during paging can shift the result set.

This causes page drift: records move between pages, so your script may skip some companies or process the same company twice, leading to incomplete or duplicated results.

---
## Throughput Analysis
**We need to ingest 25,000 records within a 4-hour window:**

4 hours equals 14,400 seconds. Each request takes on average 0.5 seconds, so a single-threaded script can process:

`1 / 0.5 = 2 requests per second`

This matches the API rate limit of 600 requests per 5 minutes, which is also 2 requests per second. At this speed, total processing time is:

`25,000 × 0.5 = 12,500 seconds`

`12,500 seconds ≈ 3.47 hours`

So yes, a single-threaded script will finish within the 4-hour window.

**However, it runs right at the limit. Any retries, slow responses, or network issues could push it past the deadline.**

To make the system reliable, the code should use an asynchronous or concurrent architecture with rate limiting. For example:

Async HTTP client with a semaphore capped at 2 requests per second:
* Worker pool with a rate limiter
* Retry handling with backoff
* This gives you better reliability, easier scaling, and protection against timing overruns.

---

## Rate Limiting Strategy: 
When a client receives a `429 Too Many Requests` response, it should not retry blindly or with a fixed delay. Instead, it should check the HTTP response headers to determine when it is safe to retry.

`Retry-After` header is defined by the HTTP specification and tells the client exactly how long it must wait before making the next request.

**A well-behaved client should:**
* Read the Retry-After header
* Sleep until the specified time
* Retry only after the delay expires
