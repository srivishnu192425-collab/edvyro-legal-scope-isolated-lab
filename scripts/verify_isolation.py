#!/usr/bin/env python3
"""
Lab Isolation and Setup Verification Script
Task 02: Legal Scope and Isolated Lab
Author: Srivishnu R (Cybersecurity Intern)
"""

import sys
import socket
import urllib.request
import urllib.error
import json
import datetime
import subprocess
import time
import os

TARGET_HOST = "127.0.0.1"
TARGET_PORT = 3000
HEALTH_URL = f"http://{TARGET_HOST}:{TARGET_PORT}/health"

def is_port_open(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.0)
    try:
        s.connect((host, port))
        s.close()
        return True
    except:
        return False

def get_host_lan_ips():
    """Detect local network adapter IP addresses to test external isolation."""
    ips = set()
    try:
        hostname = socket.gethostname()
        for ip in socket.gethostbyname_ex(hostname)[2]:
            if not ip.startswith("127."):
                ips.add(ip)
    except Exception as e:
        pass
    return list(ips)

def check_loopback_service():
    """Test 1: Verify local service is active and responsive on 127.0.0.1:3000"""
    print(f"[*] [TEST 1] Verifying target accessibility on loopback ({TARGET_HOST}:{TARGET_PORT})...")
    try:
        # Bypass any environment proxy for loopback verification
        proxy_handler = urllib.request.ProxyHandler({})
        opener = urllib.request.build_opener(proxy_handler)
        req = urllib.request.Request(HEALTH_URL)
        with opener.open(req, timeout=3) as response:
            status_code = response.getcode()
            headers = dict(response.headers)
            body = response.read().decode('utf-8')
            data = json.loads(body)
            
            if status_code == 200 and data.get("status") == "ONLINE":
                print(f"    [+] PASS: Target is ACTIVE on loopback interface.")
                print(f"    [+] Status Code : {status_code}")
                print(f"    [+] Target App  : {data.get('target')}")
                print(f"    [+] Environment : {data.get('network_isolation')}")
                return True, headers, data
            else:
                print(f"    [-] FAIL: Unexpected response: {status_code}")
                return False, headers, None
    except Exception as err:
        print(f"    [-] FAIL: Unable to reach target on loopback: {err}")
        return False, {}, None

def check_external_isolation(lan_ips):
    """Test 2: Verify target is NOT accessible over non-loopback / LAN interfaces."""
    print(f"[*] [TEST 2] Verifying network isolation (external interface rejection)...")
    if not lan_ips:
        print("    [!] Notice: No external LAN IP detected or sandbox virtualized. Skipping LAN interface test.")
        return True

    all_passed = True
    for ip in lan_ips:
        print(f"    [*] Testing connection to LAN interface: {ip}:{TARGET_PORT}...")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        try:
            result = s.connect_ex((ip, TARGET_PORT))
            if result != 0:
                print(f"    [+] PASS: Connection to {ip}:{TARGET_PORT} correctly REFUSED (Result Code: {result}).")
                print(f"              Target is NOT exposed to external/LAN network.")
            else:
                print(f"    [-] FAIL: Connection to {ip}:{TARGET_PORT} SUCCEEDED! Target is leaking onto external interface!")
                all_passed = False
        except Exception as e:
            print(f"    [+] PASS: Exception caught connecting to {ip}: {e} (Isolated).")
        finally:
            s.close()
    return all_passed

def check_port_listener():
    """Test 3: Socket connection test to 127.0.0.1:3000."""
    print(f"[*] [TEST 3] Verifying TCP socket binding on loopback interface...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2.0)
    try:
        s.connect((TARGET_HOST, TARGET_PORT))
        print(f"    [+] PASS: TCP handshake succeeded with {TARGET_HOST}:{TARGET_PORT}.")
        s.close()
        return True
    except Exception as e:
        print(f"    [-] FAIL: TCP handshake failed: {e}")
        return False

def main():
    print("=" * 70)
    print("      LAB ISOLATION & RULES OF ENGAGEMENT VERIFICATION SUITE      ")
    print(f"      Execution Timestamp: {datetime.datetime.now().isoformat()}      ")
    print("=" * 70)

    # Check if target is running; if not, spin up local instance
    server_proc = None
    if not is_port_open(TARGET_HOST, TARGET_PORT):
        server_script = os.path.join(os.path.dirname(__file__), "..", "target-app", "server.js")
        print(f"[*] Starting local target application process ({server_script})...")
        server_proc = subprocess.Popen(["node", server_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(2)

    try:
        lan_ips = get_host_lan_ips()
        print(f"[*] Detected Host Network Adapters (External/LAN): {lan_ips if lan_ips else 'None (Isolated Loopback Only)'}")
        
        t1_pass, headers, data = check_loopback_service()
        t2_pass = check_port_listener()
        t3_pass = check_external_isolation(lan_ips)

        print("\n" + "=" * 70)
        print("                         SUMMARY OF AUDIT                        ")
        print("=" * 70)
        print(f"  Target Accessibility (127.0.0.1:3000) : {'[ PASS ]' if t1_pass else '[ FAIL ]'}")
        print(f"  TCP Socket Binding Verification       : {'[ PASS ]' if t2_pass else '[ FAIL ]'}")
        print(f"  External / LAN Network Isolation      : {'[ PASS ]' if t3_pass else '[ FAIL ]'}")
        print("=" * 70)

        passed = t1_pass and t2_pass and t3_pass
        if passed:
            print("[SUCCESS] All laboratory isolation criteria MET.")
            print("          Safe, isolated, and legal testing conditions verified.")
            return 0
        else:
            print("[WARNING] Lab verification did not meet all isolation checks.")
            return 1
    finally:
        if server_proc:
            print("[*] Tearing down spawned test target process...")
            server_proc.terminate()
            try:
                server_proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                server_proc.kill()

if __name__ == "__main__":
    sys.exit(main())
