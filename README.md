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
* Programmatic Network Automation: Automated multi-device health scanning using Python requests architectures and defensive structural dictionaries.
* REST API System Operations: Comprehensive CRUD operations parsing JSON payload matrices across Centralized Controller fabrics (GET/POST/PUT/DELETE).
* Software-Defined Architecture Theory: Direct mastery of Northbound/Southbound abstraction layers, Centralized Control Planes, and Agentless configuration management.


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

| VLAN ID | Department Zone | Endpoint Inventory | Assigned DHCP Pool / Matrix |
| :--- | :--- | :--- | :--- |
| **VLAN 30** | Executive Suite | 3 Laptops, 3 IP Phones | `EXEC_POOL` (Excl: .250-.254) |
| **VLAN 50** | Finance & Payroll | 5 Desktops, 5 IP Phones | `FIN_POOL` (Excl: .250-.254) |
| **VLAN 99** | Secure Management | 3 Admin PCs, 3 IP Phones, 1 Net Printer | *Static Infrastructure IPs* |
| **VLAN 200**| HQ Telephony/Voice| Controls all office voice lines | *Option 150 -> 10.20.90.2 (Port 2000)* |
| **VLAN 888**| Data Center Core  | Master DNS, AD, File Servers | *Static Service Allocations (.1 to .3)*|

#### 🖨️ HQ Infrastructure Perimeter Allocations
* **Central Data Center DNS**: `10.20.88.1`
* **Central Active Directory**: `10.20.88.2`
* **Central File Storage**: `10.20.88.3`
* **HQ Secure Admin Printer**: `10.20.99.200` (Gateway: `10.20.99.254`)

---

## 🛣️ Inter-Site Routing & Traffic Validation Paths

To establish complete end-to-end communication across the corporate empire, static summary routing paths were engineered on the edge boundaries to streamline CPU processing overhead and enforce strict path determinism.

### 🔄 The Outbound Cross-Country Path (Toronto to New York)
When an Engineering host in Toronto (`10.10.10.5`) initiates a secure database sync request to the New York File Server (`10.20.88.3`), the traffic traverses the architecture using the following sequential Layer 3 logic hops:

1. **The Local SVI Gateway Jump**: The host identifies that the target IP lives outside its local `/24` subnet. It encapsulates the packet and forwards it to its local default gateway interface running on the Core Switch (`interface vlan 10` -> `10.10.10.254`).
2. **The Gateway of Last Resort**: The Toronto Core Switch (`YYZ-BR-CS-01`) strips the Layer 2 VLAN tag, checks its routing table, and matches the global default route statement (`ip route 0.0.0.0 0.0.0.0 10.10.90.2`). It shoots the untagged IP packet across the internal transit link out of port `G1/0/3`.
3. **The WAN Inter-Site Routing Engine**: The Toronto Edge Router (`YYZ-BR-RTR-01`) intercepts the packet on `10.10.90.2`. It parses the destination header against the cross-country static route statement (`ip route 10.20.0.0 255.255.0.0 10.0.0.2`). It immediately forwards the frame out of its WAN interface (`Gig0/0`) across the point-to-point fiber highway.
4. **The HQ Entry Decapsulation**: The New York Edge Router (`NYC-HQ-RTR-01`) receives the packet on its WAN mouth (`10.0.0.2`). It identifies the destination as part of its internal network summary map (`ip route 10.20.0.0 255.255.0.0 10.20.90.1`) and drops the traffic down the internal HQ transit wire.
5. **The Final Data Center Distribution**: The New York Core Multi-Layer Switch (`NYC-HQ-CS-01`) catches the frame on `10.20.90.1`. It identifies the destination as a directly connected local asset inside `interface vlan 888` (`10.20.88.254`). It forwards the packet at hardware line-rate speed straight out of port `Gig1/0/4` into the File Server!

---

---

## 🚀 Live Verification Status Logs
* `YYZ-BR-PC-01` ➡️ `ping 10.10.40.200` (Local Admin Printer) — **SUCCESS (100% Return, 0% Packet Loss)**
* `YYZ-BR-PC-01` ➡️ `ping 10.20.88.1` (Cross-Country HQ DNS Server) — **SUCCESS (Traversing Cryptographic Tunnel Core)**
* `YYZ-BR-RTR-01# show crypto isakmp sa` ➡️ **STATE: QM_IDLE** (Phase 1 Management Handshake Authenticated Successfully)
* `YYZ-BR-RTR-01# show crypto ipsec sa` ➡️ **STATUS: #pkts encaps/decaps > 0** (AES-256 Payload Encryption Verified Active)
* `NYC-HQ-IP-PHONE` ➡️ `telephony-service registration` — **SUCCESS (Registered, Extensions Active via Option 150 -> 10.20.90.2 on Port 2000)**
