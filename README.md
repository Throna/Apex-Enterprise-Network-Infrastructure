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

### 📚 Key Engineering Lessons Documented

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


---

## Phase 6: Disaster Recovery, Hub-and-Spoke Exploration & Gateway Redundancy

### Overview
This phase began as a hands-on hub-and-spoke crypto map exercise (adding a third branch, "London," to test multi-peer IPsec routing) and evolved into a live disaster-recovery exercise after an unplanned configuration loss on `NYC-HQ-RTR-01`, followed by the start of Layer 3 gateway redundancy (HSRP) at the Toronto distribution layer.

### 1. Hub-and-Spoke Crypto Map Exploration (London Branch)
- Built a third branch router ("London") connected to `NYC-HQ-RTR-01` via a dedicated transit link, intended to validate a hub-and-spoke IPsec topology where NYC acts as the hub relaying encrypted traffic between Toronto and London.
- Confirmed the core hub-and-spoke crypto map pattern: multiple `crypto map <name> <seq>` entries under one map name, each with its own peer and its own dedicated crypto ACL, but a shared/reusable ISAKMP policy and transform-set (since those describe capabilities, not relationships).
- **Key finding**: crypto ACLs cannot be shared across tunnels to different peers — the `match address` ACL is what ties traffic to a specific peer's crypto map sequence entry. Consolidating multiple tunnels' traffic into one ACL causes traffic to be misdirected to the wrong peer.
- **Key finding**: relayed spoke-to-spoke traffic (e.g., London → Toronto via NYC) requires the hub's crypto ACL for each tunnel to explicitly include the *other* spoke's subnet, not just the hub's own subnet — packet source/destination IPs are unchanged by decryption, so the hub's ACLs must account for all traffic transiting that specific tunnel.
- **Packet Tracer limitation discovered**: crypto maps cannot be applied to an SVI backed by an EtherSwitch network module (`no switchport` is not supported on these simulated modules, unlike real Cisco hardware where this is a documented, supported workaround). Crypto maps require a native routed interface.
- **Decision**: the London branch was removed from the topology after confirming the concept was understood and the hardware limitation was hit — the learning objective (multi-peer crypto maps, hub-and-spoke ACL scoping) was achieved without requiring a full hardware rework.

### 2. Disaster Recovery: NYC-HQ-RTR-01 Configuration Loss
- **Root cause**: a router reload (triggered while adding/removing a physical EtherSwitch module) resulted in the loss of the OSPF process, IPsec crypto configuration, and module-related interface config — despite `write memory` having been executed beforehand.
- **Diagnosis**: confirmed `show startup-config` still contained the fully correct configuration, while `show running-config` did not — indicating the reload did not properly reload startup-config into the running configuration (a Packet Tracer reload reliability issue, not a save failure).
- **Fix**: `copy startup-config running-config` — merges NVRAM's saved config directly into the active running config without requiring a further reload.
- **Standing mitigation adopted**: after any `write memory`, verify with `show startup-config` before trusting a reload to restore it; save the `.pkt` file itself as an additional safety net.
- Full OSPF process and the full crypto stack were successfully rebuilt from concept-level understanding rather than copy-paste.

### 3. Stale IPsec SA Recovery Technique
- After the config restore, `show crypto isakmp sa` showed a mismatched state between peers (YYZ: `QM_IDLE/ACTIVE`, NYC: `MM_NO_STATE/ACTIVE`) — indicating a stale Security Association blocking fresh Phase 1 negotiation.
- **Packet Tracer limitation**: `clear crypto isakmp` / `clear crypto sa` are not supported in this simulated IOS version.
- **Workaround discovered**: removing and re-applying the crypto map on the interface (`no crypto map <name>` then `crypto map <name>`) forces both peers to drop stale SA state and renegotiate Phase 1 cleanly. Confirmed both peers returned to matching `QM_IDLE/ACTIVE` state afterward.
- **Downstream effect confirmed**: centralized DHCP relay for Toronto data VLANs only succeeded once Phase 1/Phase 2 were both re-established — a device showing an APIPA address was correctly traced back to "tunnel not yet up" rather than a DHCP or ACL misconfiguration.

### 4. HSRP Gateway Redundancy (Toronto Distribution Layer) — In Progress
- **Objective**: eliminate the single point of failure at the Toronto core switch (`YYZ-BR-CS-01`).
- Added a second Layer 3 switch, `YYZ-BR-CS-02`, dual-homed to both existing access switches (`2960-24TT`, `2960-24PS`) alongside CS-01, plus a dedicated inter-switch link between CS-01 and CS-02 for HSRP hello exchange.
- Re-addressed VLAN 10 SVIs: CS-01 retained a dedicated real IP (`10.10.10.252`), CS-02 assigned `10.10.10.253`, freeing the original gateway address (`10.10.10.254`) to become the shared HSRP virtual IP — no end-device reconfiguration required.
- Configured HSRP group 10 on VLAN 10 on both switches (`standby 10 ip 10.10.10.254`); confirmed CS-01 elected Active by default, CS-02 correctly showing Standby.
- Tested and confirmed priority + preempt behavior: setting CS-02 to priority 150 with `standby 10 preempt` forced a clean, disruption-free takeover from a healthy CS-01 — virtual IP and virtual MAC remained constant throughout, requiring no ARP re-learning by end devices.
- **Remaining work**: replicate HSRP across VLANs 20, 40, 88, 99, 100; configure `standby track` against each switch's uplink; integrate CS-02 into OSPF; validate a genuine failure-triggered failover.

---

## 📚 Key Engineering Lessons Documented (Phase 6 Additions)

| Concept | Lesson |
| :--- | :--- |
| Crypto ACL Scope | Crypto ACLs are peer-specific, not reusable across tunnels — the ACL match is what routes traffic to the correct peer in a crypto map |
| Hub-and-Spoke Relay Traffic | A hub's crypto ACL for Tunnel A must include Tunnel B's subnet if Tunnel B's traffic is relayed through Tunnel A |
| Reusable vs Peer-Specific Crypto Config | ISAKMP policies and transform-sets are global/reusable across all peers; crypto ACLs and peer statements are not |
| Packet Tracer EtherSwitch Modules | Crypto maps cannot be applied to switch-module-backed SVIs in Packet Tracer; requires a native routed interface |
| `write memory` ≠ Reload-Proof | `write memory` can succeed while a subsequent `reload` still fails to restore the saved config in Packet Tracer — verify with `show startup-config` |
| Stale IPsec SA Recovery | `no crypto map` / `crypto map` re-application forces clean Phase 1/2 renegotiation when `clear crypto isakmp` isn't available |
| Symptom vs Root Cause | An APIPA address is a DHCP symptom, but the root cause can live one layer down (e.g., a VPN tunnel the DHCP relay depends on) |
| HSRP Virtual IP/MAC | The shared virtual IP and virtual MAC make failover invisible to end devices — no ARP table changes needed during a takeover |
| HSRP Election Stickiness | Priority alone only decides the *first* election with no incumbent; once Active, only a higher-priority peer WITH `preempt` can force a live takeover |
| HSRP Blind Spot | Plain HSRP hellos travel over the LAN-facing interface only — a healthy-looking Active router can still be cut off upstream, unless `standby track` is configured |

---

## Redundancy — Next Steps (Phase 6 Continuation Checklist)

- [ ] Replicate the HSRP pattern across remaining Toronto VLANs: 20, 40, 88, 99, 100
- [ ] Decide priority/preempt distribution per VLAN
- [ ] Configure `standby track` on both switches' uplink toward `YYZ-BR-RTR-01`
- [ ] Add CS-02 into OSPF
- [ ] Extend `ip helper-address` / DHCP relay config to CS-02's SVIs
- [ ] Run a genuine failure-triggered failover test
- [ ] Repeat the same HSRP pattern at NYC-HQ
- [ ] Consider dual-homing the edge router uplink as a separate future phase
- [ ] Update this section with final config details once complete
