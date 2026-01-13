# Topic
Triage and prioritization. Given a fictional situation of three individually important and urgent items, how would you triage them, and what relative priority would you give each.

It’s 09:30 AM on Thursday morning. You have just logged on to find three conflicting alerts.

• Slack (Product Manager): "The new feature launches Friday. I need you to add the 'Postcode' field to the connector by 5 PM today or we miss the release."

• Automated Alert – P1 (Critical): Nightly Ingestion Pipeline Failed. No data in customer dashboard. (Note: This customer is already in an escalated state and a churn risk).

• Email (Customer Success Manager): "ACME Widgets is furious that the dashboard data looks stale. I need you to jump on a call with us at 10:00 AM to explain this to them."

**Your Tasks**

• Outline how you act for the next hour (09:15 – 10:15).

    What do you do first?
    Who do you speak with and about what?
    What do you ignore?
    What do you need help with?

• The Response:

    o Draft your reply to the Customer Success Lead regarding the 10:00 AM meeting. (Do you accept? Decline? Negotiate? You decide).
    o Also, what does your response to the Product Manager on Slack look like?

---

# Triage and Prioritization Strategy
At 09:30 AM I'm facing three urgent and important items, but only one is truly critical from a business risk perspective.

### Priority Order

**P1 — Nightly Ingestion Pipeline Failure (Critical Incident)** \
This is the top priority because:
* Customer dashboard is broken
* The customer is already escalated
* There is an active churn risk
* This is a production outage

**P2 — ACME Widgets escalation (Customer Success call)** \
This is directly related to the failed pipeline. However, joining the call without fixing or understanding the root cause is not useful.

**P3 — Feature request for tomorrow’s release** \
Important, but not more important than a production outage and churn risk.

### Action Plan for 09:15 – 10:15
**09:15 – 09:30 (Immediate Response and Context Gathering)**
* Acknowledge all three messages immediately so stakeholders know I am engaged.
* Start incident investigation:
    * Check pipeline logs
    * Identify failure point
    * Check last successful run
    * Validate whether this affects all customers or only one

**09:30 – 09:50 (Incident Containment and Status)**
* Focus on restoring data ingestion
* If fix is quick then apply hotfix and restart pipeline
* If not quick then create workaround (manual backfill, partial restore)
* Prepare a clear status update for Customer Success

**09:50 – 10:00 (Stakeholder Alignment)**
* Send update to Customer Success with root cause (if known) and mitigation plan
* Ask if the 10:00 call can be shifted 30–60 minutes so I can bring real answers

**10:00 – 10:15** \
Either join the call if necessary or continue remediation if outage is still active

---

**What I Do First** \
I immediately start working on the P1 pipeline failure.

**Who I Speak With**
* Data / Platform Engineer (if needed) — for help debugging pipeline
* SRE / DevOps (if needed) — if infra related
* Customer Success Lead — to align on customer communication
* Product Manager — to reset expectations on the feature

**What I Ignore (Temporarily)** \
Feature development until the production incident is under control

**What I Need Help With**
* Debugging pipeline if root cause is not obvious
* Infra support if the failure is platform-related
* Customer Success handling communication while I focus on fixing
