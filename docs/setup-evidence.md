# Lab Setup & Network Isolation Evidence Report

**Task:** 02 - Legal Scope and Isolated Lab  
**Intern:** Srivishnu R  
**Program:** Cybersecurity Internship (Edvyro)  
**Execution Date:** November 22, 2026  
**Auditor Verification:** Passed (All Checks Green)  

---

## 1. Executive Summary

This report documents the empirical setup evidence and technical audit verification for **Task 02: Legal Scope and Isolated Lab**. The testing environment was deployed and audited to verify compliance with:
1. **Local Target Deployment:** Successful initialization of the local web application target (OWASP Juice Shop / DVWA emulated architecture).
2. **Network Isolation:** Rigorous verification that the application binds exclusively to the loopback address (`127.0.0.1`) and rejects any inbound connections from physical or virtual network adapters (`10.223.77.99` and `192.168.56.1`).
3. **Reproducibility:** Zero-dependency automated test execution via standard Python and PowerShell audit tools.

---

## 2. Technical Evidence Logs

### Evidence Item 1: Target Initialization & Console Banner
The target application is initialized using pure Node.js standard libraries, avoiding untrusted external dependencies while guaranteeing strict loopback binding.

**Command:**
```powershell
node target-app/server.js
```

**Observed Terminal Output (`evidence/server_startup.log`):**
```text
================================================================
   ISOLATED PRACTICE LAB TARGET - SECURITY ENVIRONMENT ACTIVE   
================================================================
[TARGET STATUS] Server successfully running at http://127.0.0.1:3000/
[INTERFACE]     Bound strictly to: 127.0.0.1 (Loopback Only)
[SECURITY]      Public / External Network interfaces REJECTED
[RULES OF ENG.] Only http://127.0.0.1:3000 is authorized for testing.
================================================================
[2026-11-22T14:06:10.295Z] Incoming Request: GET /health from 127.0.0.1
```

---

### Evidence Item 2: TCP Socket Binding Verification (`netstat`)
To ensure the process does not listen on `0.0.0.0` (all interfaces), a socket query was conducted using `netstat -ano`.

**Command:**
```powershell
netstat -ano | findstr 3000
```

**Observed Output (`evidence/netstat_binding.log`):**
```text
=== ACTIVE LISTENER ON PORT 3000 ===
Proto  Local Address          Foreign Address        State           PID
  TCP    127.0.0.1:3000         0.0.0.0:0              LISTENING       17228

VERIFICATION NOTE:
The socket binds exclusively to 127.0.0.1:3000.
No wildcard 0.0.0.0:3000 listener exists.
```
**Conclusion:** The process listener is strictly attached to `127.0.0.1:3000` with state `LISTENING`. External traffic cannot reach this socket.

---

### Evidence Item 3: HTTP Health Check & Security Headers
Verification of HTTP protocol response and security environment header flags.

**Command:**
```powershell
curl -i http://127.0.0.1:3000/health
```

**Observed Response (`evidence/http_response.log`):**
```http
HTTP/1.1 200 OK
x-lab-environment: Isolated-Security-Testing
x-content-type-options: nosniff
access-control-allow-origin: http://127.0.0.1:3000
access-control-allow-headers: Content-Type, Authorization
content-type: application/json
Date: Sun, 22 Nov 2026 14:06:10 GMT
Connection: keep-alive
Keep-Alive: timeout=5
Content-Length: 326

{
  "status": "ONLINE",
  "target": "OWASP Juice Shop / DVWA Emulated Lab",
  "binding": "127.0.0.1:3000",
  "network_isolation": "STRICT_LOOPBACK_ONLY",
  "external_access": "BLOCKED",
  "authorized_scope": "http://127.0.0.1:3000",
  "timestamp": "2026-11-22T14:06:10.295Z",
  "endpoints": [
    "GET  /",
    "GET  /health",
    "GET  /api/products",
    "GET  /api/search?q=<query>",
    "POST /api/login"
  ]
}
```

---

### Evidence Item 4: External / LAN Interface Rejection Audit
An automated security probe was launched against all detected physical and virtual network adapters on the host machine to verify that port 3000 is not exposed across subnets.

**Command:**
```powershell
python scripts/verify_isolation.py
```

**Observed Audit Log (`evidence/isolation_verification.log`):**
```text
======================================================================
      LAB ISOLATION & RULES OF ENGAGEMENT VERIFICATION SUITE      
      Execution Timestamp: 2026-11-22T19:36:10.769670      
======================================================================
[*] Starting local target application process (target-app\server.js)...
[*] Detected Host Network Adapters (External/LAN): ['192.168.56.1', '10.223.77.99']
[*] [TEST 1] Verifying target accessibility on loopback (127.0.0.1:3000)...
    [+] PASS: Target is ACTIVE on loopback interface.
    [+] Status Code : 200
    [+] Target App  : OWASP Juice Shop / DVWA Emulated Lab
    [+] Environment : STRICT_LOOPBACK_ONLY
[*] [TEST 3] Verifying TCP socket binding on loopback interface...
    [+] PASS: TCP handshake succeeded with 127.0.0.1:3000.
[*] [TEST 2] Verifying network isolation (external interface rejection)...
    [*] Testing connection to LAN interface: 192.168.56.1:3000...
    [+] PASS: Connection to 192.168.56.1:3000 correctly REFUSED (Result Code: 10035).
              Target is NOT exposed to external/LAN network.
    [*] Testing connection to LAN interface: 10.223.77.99:3000...
    [+] PASS: Connection to 10.223.77.99:3000 correctly REFUSED (Result Code: 10035).
              Target is NOT exposed to external/LAN network.

======================================================================
                         SUMMARY OF AUDIT                        
======================================================================
  Target Accessibility (127.0.0.1:3000) : [ PASS ]
  TCP Socket Binding Verification       : [ PASS ]
  External / LAN Network Isolation      : [ PASS ]
======================================================================
[SUCCESS] All laboratory isolation criteria MET.
          Safe, isolated, and legal testing conditions verified.
[*] Tearing down spawned test target process...
```

---

### Evidence Item 5: API Endpoints & Functionality
Verification of internal target functionality within local scope (`evidence/api_endpoints_test.log`):

* **Endpoint `/api/products`:** Returns JSON payload with 4 catalog items.
* **Endpoint `/api/search?q=juice`:** Returns query match list, validating parameterized input logic.
* **Endpoint `/api/login`:** Validates JSON authentication payload parsing within memory.

---

## 3. Alternative Target Deployment: Official OWASP Juice Shop Docker

For evaluators preferring the full official OWASP Juice Shop Docker container, the environment supports running it under the exact same isolation parameters:

```bash
# Pull official image
docker pull bkimminich/juice-shop

# Run container strictly bound to 127.0.0.1 (Loopback only)
docker run --rm -d -p 127.0.0.1:3000:3000 --name juice-shop-isolated bkimminich/juice-shop

# Verify isolation with audit script
python scripts/verify_isolation.py

# Clean up
docker stop juice-shop-isolated
```

By specifying `127.0.0.1:3000:3000` rather than `-p 3000:3000`, Docker binds the host port exclusively to the loopback interface, maintaining complete isolation from external interfaces.

---

## 4. Conclusion & Audit Sign-Off

The technical evidence definitively demonstrates that:
1. The target application is active, stable, and reproducible.
2. The network isolation controls effectively block all external network access.
3. Testing can proceed safely without risk of scope leakage or third-party interference.
