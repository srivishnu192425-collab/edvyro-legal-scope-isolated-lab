# Task 02: Starter Checklist & Completion Matrix

**Task:** 02 - Legal Scope and Isolated Lab  
**Objective:** Establish safe, legal, and reproducible conditions for security testing.  
**Deliverable:** Lab diagram, setup evidence, and signed personal rules-of-engagement document.  
**Intern:** Srivishnu R  
**Program:** Cybersecurity Internship (Edvyro)  
**Submission Requirement:** One public or view-only link (GitHub Repository).  

---

## Passing Checklist & Verification Matrix

Mark each required step as you finish it. All items must be checked to satisfy the task passing criteria.

### Phase 1: Local Target Setup
- [x] **Step 1.1: Target Selection & Architecture Planning**
  - Selected local practice target: OWASP Juice Shop / DVWA architecture.
  - Determined port allocation (`3000`) and loopback interface (`127.0.0.1`).
  - *Proof Link:* [target-app/server.js](../target-app/server.js)

- [x] **Step 1.2: Local Target Deployment**
  - Configured zero-dependency local Node.js target server and documented Docker alternative.
  - Verified local application initialization and endpoint readiness.
  - *Proof Link:* [docs/setup-evidence.md#evidence-item-1-target-initialization--console-banner](setup-evidence.md#evidence-item-1-target-initialization--console-banner)

---

### Phase 2: Network Isolation & Topology Documentation
- [x] **Step 2.1: Lab Isolation Enforcement**
  - Bound application socket strictly to `127.0.0.1:3000` (loopback only).
  - Ensured process does NOT bind to wildcard `0.0.0.0:3000`.
  - Verified that external network adapters (`10.223.77.99` and `192.168.56.1`) reject incoming connections on port 3000.
  - *Proof Link:* [evidence/netstat_binding.log](../evidence/netstat_binding.log) and [evidence/isolation_verification.log](../evidence/isolation_verification.log)

- [x] **Step 2.2: Visual Topology & Architecture Diagram**
  - Created Mermaid sequence/flow architecture diagram.
  - Created detailed ASCII topology map detailing host boundary, loopback interface, and blocked public networks.
  - Documented interface mapping table (IP, subnet, port, trust level).
  - *Proof Link:* [docs/lab-topology.md](lab-topology.md)

---

### Phase 3: Rules of Engagement (RoE) & Legal Boundaries
- [x] **Step 3.1: Explicit Prohibition of Unauthorized Testing**
  - Formulated the fundamental directive: strictly prohibiting testing systems not owned or controlled by the tester.
  - Embedded citations of cyber legislation (Indian IT Act 2000, US CFAA, UK Computer Misuse Act).
  - *Proof Link:* [docs/rules-of-engagement.md#1-executive-summary--code-of-conduct](rules-of-engagement.md#1-executive-summary--code-of-conduct)

- [x] **Step 3.2: Scope Boundaries Definition**
  - Defined explicit in-scope assets (`http://127.0.0.1:3000`).
  - Defined out-of-scope assets (public internet, corporate/home LAN, host operating system kernel).
  - *Proof Link:* [docs/rules-of-engagement.md#3-scope-definition](rules-of-engagement.md#3-scope-definition)

- [x] **Step 3.3: Allowed Techniques Specification**
  - Specified permissible methods: passive analysis, manual input validation (SQLi, XSS, CSRF, IDOR), local proxy analysis (ZAP/Burp).
  - *Proof Link:* [docs/rules-of-engagement.md#4-permitted-testing-techniques](rules-of-engagement.md#4-permitted-testing-techniques)

- [x] **Step 3.4: Prohibited Techniques & Exclusions**
  - Documented explicit bans on DoS/DDoS, automated volumetric fuzzing, malware, phishing, and external data exfiltration.
  - *Proof Link:* [docs/rules-of-engagement.md#5-prohibited-techniques--actions-exclusions](rules-of-engagement.md#5-prohibited-techniques--actions-exclusions)

- [x] **Step 3.5: Stop Conditions & Emergency Escalation**
  - Defined clear stop triggers: IP drift, socket binding alteration, host instability, security alerts.
  - Defined emergency response escalation workflow.
  - *Proof Link:* [docs/rules-of-engagement.md#6-stop-conditions--emergency-escalation](rules-of-engagement.md#6-stop-conditions--emergency-escalation)

- [x] **Step 3.6: Formal Signing & Ratification**
  - Digital signature block completed and ratified by Srivishnu R.
  - *Proof Link:* [docs/rules-of-engagement.md#8-formal-digital-signature--acknowledgment](rules-of-engagement.md#8-formal-digital-signature--acknowledgment)

---

### Phase 4: Setup Evidence & Verification Scripts
- [x] **Step 4.1: Automated Verification Scripting**
  - Authored automated audit suite in Python (`scripts/verify_isolation.py`) and PowerShell (`scripts/verify_isolation.ps1`).
  - Automated tests for loopback availability, socket binding, and external interface rejection.
  - *Proof Link:* [scripts/verify_isolation.py](../scripts/verify_isolation.py)

- [x] **Step 4.2: Evidence Capture & Logging**
  - Captured raw console logs, netstat outputs, HTTP response headers, and audit test outputs in `evidence/`.
  - Compiled comprehensive evidence synthesis report.
  - *Proof Link:* [docs/setup-evidence.md](setup-evidence.md)

---

### Phase 5: Submission & Repository Packaging
- [x] **Step 5.1: Consolidated Single-Link Structure**
  - Structured repository with clear navigation in root `README.md`.
  - Included all supporting documentation, source code, scripts, and logs in the same repository.
  - Ready for single public GitHub URL submission.
  - *Proof Link:* [README.md](../README.md)

---

## Verification Sign-Off

I confirm that all steps above have been executed, verified, and audited in compliance with the task requirements and guidelines.

**Intern Sign-off:** Srivishnu R  
**Date:** November 22, 2026  
**Result:** 100% COMPLETE (Ready for Submission)
