import subprocess
import time

# Configuration
VBOX_PATH = r"C:\your location"
VM_NAME = "Win11-Endpoint"
SNAPSHOT_NAME = "Clean"
GUEST_USER = "user"
GUEST_PASS = "user123"

def run_vbox(args):
    """Executes a VirtualBox management command on the host."""
    cmd = [VBOX_PATH] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 and "already powered off" not in result.stderr:
        # Suppress the expected 'not ready' spam during boot polling
        if "is not ready" not in result.stderr:
            print(f"[!] Warning/Error: {result.stderr.strip()}")
    return result

def wait_for_guest():
    """Polls the VM until the Guest Execution service is fully awake."""
    print("\n[4/6] Waiting for Windows 11 & Guest Additions service to initialize...")
    for i in range(24):  # Polls up to 120 seconds
        res = subprocess.run([
            VBOX_PATH, "guestcontrol", VM_NAME, "run",
            "--exe", r"C:\Windows\System32\cmd.exe",
            "--username", GUEST_USER,
            "--password", GUEST_PASS,
            "--", "cmd.exe", "/c", "echo ready"
        ], capture_output=True, text=True)

        if "is not ready" not in res.stderr and res.returncode == 0:
            print(f"      [+] Guest execution service is ACTIVE and READY! (waited ~{i*5}s)")
            time.sleep(5)
            return True
        print(f"      ...waiting for services ({i*5}s)")
        time.sleep(5)
    print("[!] Timed out waiting for guest execution service.")
    return False

def run_in_guest(script_path):
    """Executes a PowerShell script inside the guest VM without opening GUI."""
    print(f"[*] Executing inside guest: {script_path}")
    cmd = [
        "guestcontrol", VM_NAME, "run",
        "--exe", r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe",
        "--username", GUEST_USER,
        "--password", GUEST_PASS,
        "--wait-stdout", "--wait-stderr",
        "--",
        "powershell.exe", "-ExecutionPolicy", "Bypass", "-File", script_path
    ]
    result = run_vbox(cmd)
    if result.stdout:
        print(result.stdout)
    return result

def main():
    print("=" * 60)
    print("   AUTOMATED BLUE TEAM DETECTION & ATTACK PIPELINE")
    print("=" * 60)

    # 1. Power off if currently running
    print("\n[1/6] Ensuring VM is powered down...")
    run_vbox(["controlvm", VM_NAME, "poweroff"])
    time.sleep(3)

    # 2. Revert to baseline snapshot
    print(f"\n[2/6] Reverting {VM_NAME} to snapshot '{SNAPSHOT_NAME}'...")
    run_vbox(["snapshot", VM_NAME, "restore", SNAPSHOT_NAME])
    time.sleep(2)

    # 3. Start headless
    print(f"\n[3/6] Starting {VM_NAME} in Headless Mode (Zero GUI)...")
    run_vbox(["startvm", VM_NAME, "--type", "headless"])

    # 4. Wait intelligently for guest readiness
    if not wait_for_guest():
        print("[!] Aborting run due to guest timeout.")
        return

    # 5. Execute Seasoning Activity
    print("\n[5/6] Injecting Benign User Seasoning (Browsing, Documents)...")
    run_in_guest(r"C:\Scripts\seasoning.ps1")
    time.sleep(5)

    # 6. Execute Simulated Adversary Attacks
    print("\n[6/6] Executing Adversary Attack Emulation (Brute Force, Encoded PS, LSASS)...")
    run_in_guest(r"C:\Scripts\attacks.ps1")

    # 7. Ingestion buffer
    print("\n[*] Waiting 25 seconds for Splunk Universal Forwarder to ship logs to Ubuntu...")
    time.sleep(25)

    # 8. Teardown
    print("\n[*] Tearing down VM...")
    run_vbox(["controlvm", VM_NAME, "poweroff"])

    print("\n" + "=" * 60)
    print("   TEST CYCLE COMPLETE: ATTACK TELEMETRY READY IN SPLUNK!")
    print("=" * 60)

if __name__ == "__main__":
    main()