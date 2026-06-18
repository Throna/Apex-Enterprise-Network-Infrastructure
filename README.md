# Apex Global Enterprise Network Infrastructure Project

## 🏢 Executive Architecture Overview
This repository houses the complete production-grade network infrastructure design for Apex Global. The architecture features a dual-site deployment bridging a high-performance corporate headquarters in **New York (NYC-HQ)** with a regional satellite office in **Toronto (YYZ-BR)** over a dedicated cross-country WAN point-to-point transit link. 

The entire framework was designed using a **Top-Down Backbone-First Model** to guarantee absolute stability, deterministic routing boundaries, and isolated fault domains.

---

## 🛠️ Core Infrastructure Stack & Technologies Used
* **Layer 3 Core Routing**: Cisco IOS 2911 Inter-Site WAN Processing, Static/Summary routing protocols, Gateway of Last Resort engineering.
* **Multi-Layer Switching**: Cisco 3560 Switch Virtual Interfaces (SVIs), native Layer 3 hardware routing, inter-VLAN distribution.
* **Automated Network Services**: Multi-pool Cisco IOS DHCP engines, isolated infrastructure exclusions, DHCP Option 150 voice parameter targeting.
* **Unified Communications (VoIP)**: Cisco CallManager Express (CME) software integration, global telephony service engines, auto-registration matrices.
* **Layer 2 Edge Protection**: 802.1Q encapsulation trunking, VTP Domain isolation, Spanning-Tree PortFast, and edge BPDU Guard enforcement.

---


## 🤖 Collaboration & Engineering Methodology
This infrastructure was designed and validated using an advanced interactive engineering model. 
* **Lead Network Architect**: [Naeem/Thr0na] — Hand-coded all Cisco IOS router scripts, Layer 3 SVI configurations, switch port range mappings, and handled all live network troubleshooting.
* **AI Collaborator Engine**: Used to mimic real-world senior code audits, verify configuration syntax constraints against Cisco exam blueprints, and format the technical project documentation into a standardized Markdown structure.


---


## 📊 Global Enterprise Addressing Blueprints

### 🍁 Toronto Branch Matrix (YYZ-BR)
* **Inter-Site WAN Gateway Link**: `10.0.0.1/30`
* **Switch-to-Router Transit Link**: `10.10.90.1/30`
* **Local Gateway Allocation**: `.254` (Configured via Layer 3 SVIs)

| VLAN ID | Department Zone | IP Network Block | Assigned DHCP Pool |
| :--- | :--- | :--- | :--- |
| **VLAN 10** | Engineering Data | `10.10.10.0/24` | `ENG_POOL` (Excl: .250-.254) |
| **VLAN 20** | Sales Department | `10.10.20.0/24` | `SLS_POOL` (Excl: .250-.254) |
| **VLAN 40** | Administration | `10.10.40.0/24` | `ADM_POOL` (Excl: .250-.254) |
| **VLAN 88** | Local Web Server | `10.10.88.0/24` | *Static Allocation: 10.10.88.1* |
| **VLAN 99** | Secure Management| `10.10.99.0/24` | *Static Infrastructure Switch IPs* |
| **VLAN 100**| Telephony/Voice | `10.10.100.0/24`| `VOICE_POOL` (Option 150 -> .90.2) |

---

### 🗽 New York Headquarters Matrix (NYC-HQ)
* **Inter-Site WAN Gateway Link**: `10.0.0.2/30`
* **Switch-to-Router Transit Link**: `10.20.90.1/30`
* **Local Gateway Allocation**: `.254` (Configured via Layer 3 SVIs)

| VLAN ID | Department Zone | IP Network Block | Assigned DHCP Pool / Matrix |
| :--- | :--- | :--- | :--- |
| **VLAN 30** | Executive & Legal | `10.20.30.0/24` | `EXEC_POOL` (Excl: .250-.254) |
| **VLAN 50** | Finance & Payroll | `10.20.50.0/24` | `FIN_POOL` (Excl: .250-.254) |
| **VLAN 99** | Secure Management | `10.20.99.0/24` | *Static Infrastructure Switch IPs* |
| **VLAN 200**| HQ Telephony/Voice| `10.20.200.0/24`| *Option 150 -> 10.20.90.2 (Port 2000)* |
| **VLAN 888**| Data Center Core  | `10.20.88.0/24` | *Static Service Allocations (.1 to .3)*|

* **NYC-HQ-SRV-DNS**: `10.20.88.1`
* **NYC-HQ-SRV-AD**: `10.20.88.2`
* **NYC-HQ-SRV-FILE**: `10.20.88.3`
