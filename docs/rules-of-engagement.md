# Authorised Lab Rules of Engagement (RoE)

**Document Type:** Formal Security Rules of Engagement & Code of Ethics  
**Task:** 02 - Legal Scope and Isolated Lab  
**Author & Signatory:** Srivishnu R (Cybersecurity Intern)  
**Organization / Program:** Edvyro Cybersecurity Internship  
**Effective Date:** November 22, 2026  
**Document Version:** 1.0.0 (Binding)  

---

## 1. Executive Summary & Code of Conduct

This **Rules of Engagement (RoE)** document establishes the formal boundaries, legal authorizations, permitted techniques, explicit prohibitions, and operational stop conditions governing all security testing activities conducted by **Srivishnu R**.

### Mandatory Ethical Commitment
> **FUNDAMENTAL DIRECTIVE:**  
> **Under NO circumstances shall any security assessment, scanning, exploitation, probing, or testing be performed against any system, network, host, domain, or device that is NOT owned, leased, or explicitly authorized in writing by the owner.**  
> Testing unauthorized third-party infrastructure constitutes an illegal breach under global cybercrime statutes. All testing activities must remain 100% confined to the locally isolated practice laboratory.

---

## 2. Legal Authority and Statutory Framework

All activities conducted within this laboratory operate under explicit personal and academic authorization strictly for educational and vulnerability analysis purposes within a sandbox.

The signatory acknowledges and adheres strictly to the following cyber legislation and ethical standards:
1. **Indian Information Technology Act, 2000 (Amended 2008):** Sections 43 (Penalty and compensation for damage to computer system) and 66 (Computer related offences / Hacking).
2. **United States Computer Fraud and Abuse Act (CFAA) (18 U.S.C. § 1030):** Prohibition against accessing protected computers without authorization.
3. **United Kingdom Computer Misuse Act 1990:** Sections 1 to 3 regarding unauthorized access to computer material and unauthorized acts with intent to impair computer operations.
4. **OWASP Code of Ethics:** Integrity, confidentiality, professional responsibility, and defense of systems.

---

## 3. Scope Definition

### 3.1 Strictly In-Scope Assets
Testing is permitted **ONLY** on the following locally hosted and isolated asset:

| Scope Asset Identifier | Target Type | Interface / Host | Port(s) | Protocol | Boundary Constraint |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Local Practice Target** | OWASP Juice Shop / DVWA Lab | `127.0.0.1` (`localhost`) | `3000` | HTTP | Local Loopback ONLY |
| **Local Mock API Endpoints** | REST Endpoints (`/api/*`) | `127.0.0.1` (`localhost`) | `3000` | HTTP | In-Process Memory Only |

### 3.2 Strictly Out-of-Scope Assets (Zero Tolerance)
The following targets are **EXPLICITLY EXCLUDED** from testing:

* ❌ **Public Internet Assets:** Any public IP, domain, third-party web service, cloud resource, or DNS resolver.
* ❌ **Local Area Network (LAN):** Any other device on the subnet (e.g., `10.223.77.0/24`, `192.168.56.0/24`), default router gateway (`10.223.77.1`), or neighboring student/workstation machines.
* ❌ **Host Operating System Core:** Host OS drivers, Windows kernel, system services, registry, or security software (antivirus/EDR).
* ❌ **External APIs / Integrations:** Any third-party payment gateways, OAuth providers, or analytics services.

---

## 4. Permitted Testing Techniques

Testing is limited to application security testing methodologies targeting vulnerabilities within the isolated web application:

1. **Passive Reconnaissance & Code Inspection:**
   - Reviewing client-side JavaScript, HTML, CSS, and API endpoints.
   - Inspecting HTTP headers, cookies, and CORS configurations.
2. **Manual Input Validation & Sanitization Testing:**
   - Testing for Structured Query Language Injection (SQLi) on local query parameters.
   - Testing for Cross-Site Scripting (Reflected / Stored XSS) on local input fields.
   - Cross-Site Request Forgery (CSRF) and Broken Object Level Authorization (BOLA/IDOR).
3. **Local Intercept Proxying:**
   - Intercepting HTTP traffic using a local instance of OWASP ZAP or Burp Suite bound strictly to `127.0.0.1:8080` targeting `127.0.0.1:3000`.
4. **Session & Authentication Logic Testing:**
   - Testing session token creation, expiration, and role-based access controls within the local target database.

---

## 5. Prohibited Techniques & Actions (Exclusions)

The following activities are strictly prohibited at all times:

1. **Denial of Service (DoS / DDoS):**
   - High-volume thread stress testing, network packet flooding (SYN flood, UDP flood), application crash exhaustion attacks.
2. **Automated Volumetric Brute-Forcing:**
   - Unthrottled credential spraying, directory fuzzing without rate limits that could destabilize the host workstation.
3. **Network Layer Attacks:**
   - ARP poisoning, DNS spoofing, packet sniffing on external network adapters.
4. **Malware & Persistent Payloads:**
   - Crafting, executing, or storing self-replicating worms, ransomware, rootkits, or destructive payloads.
5. **Social Engineering & Phishing:**
   - Phishing emails, pretexting, or credential harvesting targeting any human user.
6. **Data Exfiltration:**
   - Egressing any lab data to external servers, cloud buckets, or command-and-control (C2) servers.

---

## 6. Stop Conditions & Emergency Escalation

Testing must be **TERMINATED IMMEDIATELY** if any of the following stop conditions are met:

```
+------------------------------------------------------------------------+
|                          STOP CONDITIONS                               |
+------------------------------------------------------------------------+
| 1. IP / Network Drift:                                                 |
|    Any request resolves to or egresses towards an IP outside 127.0.0.1 |
| 2. Socket Binding Alteration:                                          |
|    Target socket changes from 127.0.0.1 to 0.0.0.0 (Wildcard exposure) |
| 3. Host System Instability:                                            |
|    Host CPU / memory exhaustion, unexpected freeze, or crash          |
| 4. Security Incident Detection:                                        |
|    Antivirus / EDR alerts, unauthorized persistent file generation     |
| 5. Scope Ambiguity:                                                    |
|    Any uncertainty regarding authorization on an endpoint or service   |
+------------------------------------------------------------------------+
```

### Emergency Escalation Protocol:
1. **Immediate Cessation:** Execute `scripts/teardown_lab.ps1` or terminate the target process.
2. **Isolation Enforcement:** Disconnect physical/virtual network adapters if any unintended network activity is observed.
3. **Incident Logging:** Document the timestamp, exact command/payload executed, and system behavior.
4. **Supervisor Notification:** Inform the internship mentor / academic coordinator with the incident log.

---

## 7. Standard Finding & Vulnerability Reporting Template

Whenever an authorized finding is discovered within the lab, it must be documented using the following standardized schema:

```markdown
### Finding ID: VULN-[YEAR]-[001]
- **Vulnerability Title:** [e.g., Unauthenticated SQL Injection in Search Endpoint]
- **Severity Rating:** [Critical / High / Medium / Low / Informational] (CVSS v3.1)
- **Target Endpoint:** http://127.0.0.1:3000/api/search?q=[payload]
- **Date & Time Identified:** YYYY-MM-DD HH:MM:SS UTC
- **Vulnerability Classification:** CWE-[ID] (e.g., CWE-89: SQL Injection)
- **Description:** [Concise description of the flaw and root cause]
- **Proof of Concept (PoC):**
  ```http
  GET /api/search?q=' OR 1=1-- HTTP/1.1
  Host: 127.0.0.1:3000
  ```
- **Business / System Impact:** [Data leakage, unauthorized privilege escalation]
- **Remediation Recommendation:** [Parameterized queries, prepared statements, input sanitization]
```

---

## 8. Formal Digital Signature & Acknowledgment

By signing below, I certify that I have read, understood, and agreed to abide strictly by these Rules of Engagement. I confirm that all security testing conducted during this internship is restricted to systems I own or have written authorization to test, specifically the isolated local practice target.

| Field | Detail |
| :--- | :--- |
| **Signatory Name** | **Srivishnu R** |
| **Role / Title** | Cybersecurity Intern / Security Analyst |
| **Internship Program** | Edvyro Cybersecurity Internship |
| **Task Reference** | Task 02: Legal Scope and Isolated Lab |
| **Date of Signing** | November 22, 2026 |
| **Commitment Hash** | `SHA256: d84a92c10b7f83e843c08bf60d1947b198c2579173eb8b261173693e506ab95e` |
| **Signature Status** | **SIGNED & RATIFIED (ACTIVE)** |

**Signature:**  
*Srivishnu R*  
*(Digitally Committed to Version Control)*
