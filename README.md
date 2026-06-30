# Apex Global Enterprise Network Infrastructure Project

## 🏢 Executive Architecture Overview
This repository houses the complete production-grade network infrastructure design for Apex Global. The architecture features a dual-site deployment bridging a high-performance corporate headquarters in **New York (NYC-HQ)** with a regional satellite office in **Toronto (YYZ-BR)** over a dedicated cross-country WAN point-to-point transit link.

The entire framework was designed using a **Top-Down Backbone-First Model** to guarantee absolute stability, deterministic routing boundaries, and isolated fault domains.

---

## 🛠️ Core Infrastructure Stack & Technologies Used
* **Layer 3 Core Routing**: Cisco IOS 2911 Inter-Site WAN Processing, OSPF Dynamic Routing (Area 0 Backbone), Static/Summary routing protocols, Gateway of Last Resort engineering.
* **Multi-Layer Switching**: Cisco 3560 Switch Virtual Interfaces (SVIs), native Layer 3 hardware routing, inter-VLAN distribution.
* **Automated Network Services**: Multi-pool Cisco IOS DHCP engines, isolated infrastructure exclusions, DHCP Option 150 voice parameter targeting, centralized DHCP relay via `ip helper-address`.
* **Unified Communications (VoIP)**: Cisco CallManager Express (CME) software integration, global telephony service engines, auto-registration matrices.
* **Layer 2 Edge Protection**: 802.1Q encapsulation trunking, VTP Domain isolation, Spanning-Tree PortFast, and edge BPDU Guard enforcement.
* **Network Security**: Site-to-site IPsec VPN (AES-256/SHA/DH Group 5), Extended ACL traffic classification, NAT/PAT overload with VPN exclusion logic.
* **Programmatic Network Automation**: Automated multi-device health scanning using Python requests architectures and defensive structural dictionaries.
* **REST API System Operations**: Comprehensive CRUD operations parsing JSON payload matrices across Centralized Controller fabrics (GET/POST/PUT/DELETE).
* **Software-Defined Architecture Theory**: Direct mastery of Northbound/Southbound abstraction layers, Centralized Control Planes, and Agentless configuration management.

---

## 🤖 Collaboration & Engineering Methodology
This infrastructure was designed and validated using an advanced interactive engineering model.
* **Lead Network Architect**: [Naeem/Thr0na] — Hand-coded all Cisco IOS router scripts, Layer 3 SVI configurations, switch port range mappings, and handled all live network troubleshooting. All configuration decisions, verification, and debugging were performed and validated by the lead architect directly in Packet Tracer CLI.
* **AI Collaborator Engine**: Used to mimic real-world senior engineer code audits, verify configuration syntax constraints against Cisco exam blueprints, assist with structured troubleshooting methodology, and format technical project documentation into standardized Markdown structure. All AI suggestions were critically evaluated, tested, and either validated or rejected by the lead architect based on live network behavior.

---

## 📊 Global Enterprise Addressing Blueprints

### 🍁 Toronto Branch Matrix (YYZ-BR)

- **Inter-Site WAN Gateway Link**: 10.0.0.1/30
- **Switch-to-Router Transit Link**: 10.10.90.1/30 (Core Switch G1/0/3 ➡ Edge Router G0/1)
- **Local Gateway Allocation**: .254 (Configured via Layer 3 SVIs)

| VLAN ID | Department Zone | IP Network Block | Assigned DHCP Pool |
| :--- | :--- | :--- | :--- |
| **VLAN 10** | Engineering Data | `10.10.10.0/24` | Centralized NYC DHCP Server |
| **VLAN 20** | Sales Department | `10.10.20.0/24` | Centralized NYC DHCP Server |
| **VLAN 40** | Administration | `10.10.40.0/24` | Centralized NYC DHCP Server |
| **VLAN 99** | Secure Management | `10.10.99.0/24` | Static Infrastructure Switch IPs |
| **VLAN 100** | Telephony/Voice | `10.10.100.0/24` | `VOICE_POOL` Local on YYZ Edge Router (Option 150 -> 10.10.90.2) |

### 🗽 New York Headquarters Matrix (NYC-HQ)
* **Inter-Site WAN Gateway Link**: `10.0.0.2/30`
* **Switch-to-Router Transit Link**: `10.20.90.1/30`
* **Local Gateway Allocation**: `.254` (Configured via Layer 3 SVIs)

| VLAN ID | Department Zone | Endpoint Inventory | Assigned DHCP Pool / Matrix |
| :--- | :--- | :--- | :--- |
| **VLAN 30** | Executive Suite | 3 Laptops, 3 IP Phones | `EXEC_POOL` (Excl: .250-.254) |
| **VLAN 50** | Finance & Payroll | 5 Desktops, 5 IP Phones | `FIN_POOL` (Excl: .250-.254) |
| **VLAN 99** | Secure Management | 3 Admin PCs, 3 IP Phones, 1 Net Printer | Static Infrastructure IPs |
| **VLAN 200** | HQ Telephony/Voice | Controls all office voice lines | Option 150 -> 10.20.90.2 (Port 2000) |
| **VLAN 888** | Data Center Core | Master DNS, AD, File Servers | Static Service Allocations (.1 to .3) |

#### 🖨️ HQ Infrastructure Perimeter Allocations
* **Central Data Center DNS / DHCP Server**: `10.20.88.1`
* **Central Active Directory**: `10.20.88.2`
* **Central File Storage**: `10.20.88.3`
* **HQ Secure Admin Printer**: `10.20.99.200` (Gateway: `10.20.99.254`)

---

## 🛣️ Inter-Site Routing & Traffic Validation Paths

### 🔄 The Outbound Cross-Country Path (Toronto to New York)
With OSPF now handling dynamic routing, when an Engineering host in Toronto (`10.10.10.5`) initiates a secure database sync request to the New York File Server (`10.20.88.3`), the traffic traverses the architecture using the following sequential Layer 3 logic hops:

1. **The Local SVI Gateway Jump**: The host identifies that the target IP lives outside its local `/24` subnet and forwards it to its default gateway (`interface vlan 10` -> `10.10.10.254`) on the Core Switch.
2. **Dynamic OSPF Routing Decision**: The Toronto Core Switch checks its OSPF-learned routing table and forwards the packet across the internal transit link (`10.10.90.0/30`) to the Edge Router.
3. **The WAN Inter-Site Routing Engine**: The Toronto Edge Router (`YYZ-BR-RTR-01`) matches the OSPF-learned route to New York and forwards the frame out of its WAN interface (`Gig0/0`) across the point-to-point link, encrypted inside the IPsec VPN tunnel.
4. **The HQ Entry Decapsulation**: The New York Edge Router (`NYC-HQ-RTR-01`) decrypts the packet and routes it internally via OSPF toward the core switch.
5. **The Final Data Center Distribution**: The New York Core Switch delivers the packet to the File Server at hardware line-rate via `interface vlan 888`.

---

## 🚀 Live Verification Status Logs
* `YYZ-BR-PC-01` ➡️ `ping 10.10.40.200` (Local Admin Printer) — **SUCCESS (100% Return, 0% Packet Loss)**
* `YYZ-BR-PC-01` ➡️ `ping 10.20.88.1` (Cross-Country HQ DNS Server) — **SUCCESS (Traversing IPsec VPN Tunnel)**
* `YYZ-BR-RTR-01# show crypto isakmp sa` ➡️ **STATE: QM_IDLE** (Phase 1 Handshake Authenticated Successfully)
* `YYZ-BR-RTR-01# show crypto ipsec sa` ➡️ **STATUS: #pkts encaps/decaps > 0** (AES-256 Encryption Verified Active)
* `YYZ-BR-RTR-01# show ip ospf neighbor` ➡️ **3.3.3.3 FULL/- on Gig0/0** (Cross-Country OSPF Adjacency Active)
* `YYZ-BR-RTR-01# show ip route ospf` ➡️ **O 10.20.x.x routes populating** (Dynamic Route Learning Confirmed)
* `YYZ-BR-PHN-1001` ➡️ `telephony-service registration` — **SUCCESS (IP: 10.10.100.x, Extension Active, Option 150 Verified)**
* `NYC-HQ-IP-PHONE` ➡️ `telephony-service registration` — **SUCCESS (Registered, Extensions Active via Option 150 -> 10.20.90.2)**

---

# Engineering Logbook

## Phase 4: Network Infrastructure Upgrade

### 1. Centralized DHCP Server Architecture Migration
- Completely decommissioned localized data DHCP pools (`ENG_POOL`, `SLS_POOL`, `ADM_POOL`) from the Toronto multi-layer switch core to achieve a 100% centralized data architecture.
- Retained local `VOICE_POOL` on the Toronto Edge Router (`YYZ-BR-RTR-01`) to guarantee Local Voice Survivability in the event of cross-country WAN dropouts.
- Provisioned master data scopes on the centralized New York Data Center Server (`10.20.88.1`) to service all Toronto branch data subnets via DHCP relay.

### 2. Layer 3 Cross-Country DHCP Relay Pipelines
- Applied `ip helper-address 10.20.88.1` across all Toronto branch SVI interfaces (VLAN 10, 20, 40, 99) to relay data DHCP requests to the NYC centralized server across the IPsec VPN tunnel.
- Confirmed the relay mechanism leverages the GIADDR header stamp to correctly distinguish and allocate distinct `10.10.X.X` Toronto subnets from the New York server.
- Retained local `ip helper-address 10.10.90.2` on VLAN 100 SVI to relay voice DHCP requests to the local `VOICE_POOL` on the Toronto Edge Router.

### 3. Network Address Translation (NAT/PAT Overload) Deployment
- Constructed a simulated ISP backbone (`ISP-GLOBAL-RTR`) using real-world documentation IP space: `203.0.113.0/30` for Toronto and `198.51.100.0/30` for New York.
- Established PAT boundaries on both edge routers using `ip nat inside`/`ip nat outside` interface designations.
- Engineered an extended ACL (`NAT_TRAFFIC`) to replace the original standard ACL, implementing explicit VPN traffic exclusion logic to prevent NAT from intercepting IPsec-destined packets:
```
ip access-list extended NAT_TRAFFIC
 deny udp any any eq bootps
 deny udp any any eq bootpc
 deny ip 10.10.0.0 0.0.255.255 10.20.0.0 0.0.255.255
 deny ip 10.10.0.0 0.0.255.255 10.10.0.0 0.0.255.255
 permit ip 10.10.0.0 0.0.255.255 any
```

### 4. Layer 2 Spanning-Tree & Port-Security Stabilization
- Identified and resolved a Port Security conflict where `switchport port-security mac-address sticky` was incorrectly deployed across 802.1Q trunk links.
- Decommissioned Port Security from all core uplinks.
- Restored `switchport voice vlan 100` mapping symmetry across all access switches.
- Applied `spanning-tree portfast` to all end-device facing access ports to prevent STP convergence delay from timing out DHCP requests on phone power-up.

---

## Phase 5: OSPF Dynamic Routing Implementation

### Overview
Migrated the entire inter-site and intra-site routing architecture from rigid static routes to OSPF (Open Shortest Path First) Process 1, Area 0 backbone. This gives the network a living routing brain — routers now dynamically discover topology changes and recalculate paths automatically in the event of link failures.

### OSPF Router ID Assignment
| Device | Role | OSPF Router ID |
| :--- | :--- | :--- |
| YYZ-BR-RTR-01 | Toronto Edge Router | 1.1.1.1 |
| YYZ-BR-CS-01 | Toronto Core Switch | 2.2.2.2 |
| NYC-HQ-RTR-01 | New York Edge Router | 3.3.3.3 |
| NYC-HQ-CS-01 | New York Core Switch | 4.4.4.4 |

### Implementation Steps

**Step 1 — Local OSPF activation on all four devices:**
- Configured `router ospf 1` with unique router IDs on all devices
- Applied `passive-interface` on all internet-facing ports (`Gig0/2`) to prevent OSPF hellos from leaking to the ISP
- Advertised all internal networks and transit links into Area 0

**Step 2 — Cross-country OSPF adjacency:**
- Identified that OSPF multicast hellos (`224.0.0.5`) cannot traverse a pure IPsec tunnel because the Crypto ACL only permits unicast traffic matching the defined interesting traffic selectors
- Resolution: Applied `ip ospf network point-to-point` on both edge router WAN interfaces (`Gig0/0`) to bypass DR/BDR election and allow direct unicast hello exchange
- Added the WAN transit subnet (`10.0.0.0/30`) to both routers' Crypto ACL 110 to permit OSPF packets through the VPN tunnel
- Confirmed full OSPF adjacency: `3.3.3.3 FULL/- on GigabitEthernet0/0`

**Step 3 — Static route cleanup:**
- Removed redundant static routes superseded by OSPF (`no ip route 10.20.0.0 255.255.0.0 10.0.0.2`)
- Verified OSPF routes (`O`) populated correctly in routing tables on all devices

### Key Troubleshooting Challenges Resolved
- **IPsec vs OSPF Multicast Conflict**: OSPF hellos use multicast destination `224.0.0.5` which doesn't match standard unicast Crypto ACL rules and gets dropped. Solved by combining `ip ospf network point-to-point` with WAN subnet inclusion in ACL 110.
- **Administrative Distance Override**: Static routes (AD=1) suppress OSPF routes (AD=110) for the same destination. Resolved by removing conflicting statics after OSPF convergence was confirmed.
- **NAT Before Crypto Ordering**: Cisco processes NAT before the crypto map. Toronto-to-NYC traffic was being NATted to the public IP before the VPN could encrypt it. Resolved by upgrading NAT ACL from standard to extended, with explicit deny rules for VPN-destined traffic.
- **DHCP Relay Typo**: A single digit typo in the VLAN 100 `ip helper-address` (`10.0.90.2` instead of `10.10.90.2`) caused all voice DHCP requests to be routed toward the WAN instead of the local VOICE_POOL. Identified via Packet Tracer simulation mode packet tracing.

---

## 📚 Key Engineering Lessons Documented

| Concept | Lesson |
| :--- | :--- |
| OSPF + IPsec | OSPF multicasts can't traverse pure IPsec tunnels without GRE or point-to-point network type override |
| NAT Order of Operations | NAT is processed before the crypto map — VPN traffic must be explicitly excluded from NAT ACLs |
| Standard vs Extended ACL | Standard ACLs filter source only; Extended ACLs filter source AND destination — required for NAT exclusion logic |
| ACL Direction | ACL direction is always from the router interface's perspective, never the network's perspective |
| Administrative Distance | Lower AD wins: Static=1 always beats OSPF=110 for the same destination |
| ip helper-address | Required whenever DHCP client and server are on different subnets, even one hop away |
| PortFast | Mandatory on all end-device ports — without it, STP convergence delay causes DHCP timeouts on device power-up |
| Version Control | Always `copy run start` and backup configs externally before making changes — a working rollback point is worth more than any feature |
