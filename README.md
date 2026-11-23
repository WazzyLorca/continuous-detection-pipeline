# Continuous Detection & Adversary Emulation Pipeline

An automated detection engineering and adversary emulation test harness built using Python, VirtualBox CLI (`VBoxManage`), Microsoft Sysmon, and Splunk Enterprise.

The pipeline automates the entire lifecycle of an enterprise endpoint: reverting to a clean baseline snapshot, launching headless, injecting benign user seasoning, triggering simulated cyberattacks mapped to **MITRE ATT&CK**, ingesting granular telemetry into a SIEM, and performing automated teardown.

---

## Architecture Diagram

```mermaid
flowchart TD
    subgraph Host ["Physical Host (Windows)"]
        Orch["Python Orchestrator (orchestrator.py)"]
        VBoxCLI["VBoxManage CLI"]
        Orch --> VBoxCLI
    end

    subgraph Net ["Isolated NAT Network (SOC-Net)"]
        subgraph Target ["Win11-Endpoint (Target VM)"]
            Sysmon["Sysmon (Process & Kernel Telemetry)"]
            UF["Splunk Universal Forwarder (LocalSystem)"]
            Attacks["Adversary Emulation (attacks.ps1)"]
            Season["User Seasoning (seasoning.ps1)"]
            Attacks --> Sysmon
            Season --> Sysmon
            Sysmon --> UF
        end

        subgraph SIEM ["Ubuntu SIEM (Splunk Enterprise)"]
            Docker["Splunk Enterprise (Docker Container)"]
            Port9997["TCP Port 9997 (Log Ingestion)"]
            Web8000["TCP Port 8000 (SPL Analytics)"]
            UF -->|TCP 9997| Port9997
            Port9997 --> Docker
        end
    end

    VBoxCLI -->|Snapshot Revert & Headless Boot| Target
    VBoxCLI -->|guestcontrol Execution| Attacks
    VBoxCLI -->|guestcontrol Execution| Season