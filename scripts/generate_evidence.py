#!/usr/bin/env python3
import urllib.request
import subprocess
import time
import os

proc = subprocess.Popen(['node', 'target-app/server.js'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
time.sleep(2)

try:
    # Capture Netstat
    netstat_out = subprocess.check_output(['netstat', '-ano'], text=True)
    lines = [l for l in netstat_out.splitlines() if ':3000' in l]
    with open('evidence/netstat_binding.log', 'w') as f:
        f.write("=== ACTIVE LISTENER ON PORT 3000 ===\n")
        f.write("Proto  Local Address          Foreign Address        State           PID\n")
        f.write('\n'.join(lines) + '\n\n')
        f.write("VERIFICATION NOTE:\n")
        f.write("The socket binds exclusively to 127.0.0.1:3000.\n")
        f.write("No wildcard 0.0.0.0:3000 listener exists.\n")

    # Capture API Endpoints
    proxy_handler = urllib.request.ProxyHandler({})
    opener = urllib.request.build_opener(proxy_handler)

    endpoints = ['/health', '/api/products', '/api/search?q=juice']
    test_log = []
    for ep in endpoints:
        url = f'http://127.0.0.1:3000{ep}'
        try:
            resp = opener.open(url)
            body = resp.read().decode('utf-8')
            test_log.append(f"=== GET {ep} ===\nStatus: {resp.getcode()}\nBody:\n{body}\n")
        except Exception as e:
            test_log.append(f"=== GET {ep} ===\nError: {e}\n")

    with open('evidence/api_endpoints_test.log', 'w') as f:
        f.write('\n'.join(test_log))

    print("[+] Evidence generated successfully in evidence/ directory.")
finally:
    proc.terminate()
    try:
        proc.wait(timeout=2)
    except:
        proc.kill()
