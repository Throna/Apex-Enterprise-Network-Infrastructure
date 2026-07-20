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
* **High Availability**: HSRP gateway redundancy with load-shared priorities, interface tracking, and dual-homed core switch uplinks at both sites.
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
- **Redundant Switch-to-Router Transit Link**: 10.10.91.0/30 (Core Switch CS-02 ➡ Edge Router HWIC-1GE-SFP, added in Phase 6)
- **Local Gateway Allocation**: .254 (Configured via Layer 3 SVIs, HSRP virtual IP as of Phase 6)

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
* **Redundant Switch-to-Router Transit Link**: `10.20.91.0/30` (Core Switch CS-02 ➡ Edge Router HWIC-1GE-SFP, added in Phase 6)
* **Local Gateway Allocation**: `.254` (Configured via Layer 3 SVIs, HSRP virtual IP as of Phase 6)

| VLAN ID | Department Zone | Endpoint Inventory | Assigned DHCP Pool / Matrix |
| :--- | :--- | :--- | :--- |
| **VLAN 30** | Executive Suite | 3 Laptops, 3 IP Phones | `EXEC_POOL` (Excl: .250-.254) |
| **VLAN 33** | Wireless (WLC) | WLC + AP + wireless clients | Static/DHCP via WLC |
| **VLAN 44** | (see live config) | — | — |
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

1. **The Local SVI Gateway Jump**: The host identifies that the target IP lives outside its local `/24` subnet and forwards it to its default gateway (`interface vlan 10` -> `10.10.10.254`, the HSRP virtual IP) on whichever core switch currently holds Active status for that VLAN.
2. **Dynamic OSPF Routing Decision**: The Toronto Core Switch checks its OSPF-learned routing table and forwards the packet across one of two available transit links (`10.10.90.0/30` or, as of Phase 6, `10.10.91.0/30`) to the Edge Router.
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
* `show standby brief` (both sites) ➡️ **Live failure-triggered failover test PASSED** — tracked uplink shutdown correctly triggered automatic HSRP failover; interface recovery correctly triggered automatic reclaim via preempt (see Phase 6)

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
| NYC-HQ-CS-02 | New York Core Switch (Redundant, added Phase 6) | 5.5.5.5 |
| YYZ-BR-CS-02 | Toronto Core Switch (Redundant, added Phase 6) | 6.6.6.6 |

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
This phase began as a hands-on hub-and-spoke crypto map exercise (adding a third branch, "London," to test multi-peer IPsec routing) and evolved into a live disaster-recovery exercise after an unplanned configuration loss on `NYC-HQ-RTR-01`, followed by a full build-out of Layer 3 gateway redundancy (HSRP) at both sites, completed and verified with a live failover test.

### 1. Hub-and-Spoke Crypto Map Exploration (London Branch) — Built, Tested, and Subsequently Removed

*Note: The London branch described below was a temporary learning exercise and is no longer part of the live topology. It is retained here because the concepts validated during its build (multi-peer crypto maps, hub-and-spoke ACL scoping) are part of this project's engineering record and directly informed later design decisions.*

- Built a third branch router ("London") connected to `NYC-HQ-RTR-01` via a dedicated transit link, intended to validate a hub-and-spoke IPsec topology where NYC acts as the hub relaying encrypted traffic between Toronto and London.
- Confirmed the core hub-and-spoke crypto map pattern: multiple `crypto map <name> <seq>` entries under one map name, each with its own peer and its own dedicated crypto ACL, but a shared/reusable ISAKMP policy and transform-set (since those describe capabilities, not relationships).
- **Key finding**: crypto ACLs cannot be shared across tunnels to different peers — the `match address` ACL is what ties traffic to a specific peer's crypto map sequence entry. Consolidating multiple tunnels' traffic into one ACL causes traffic to be misdirected to the wrong peer.
- **Key finding**: relayed spoke-to-spoke traffic (e.g., London → Toronto via NYC) requires the hub's crypto ACL for each tunnel to explicitly include the *other* spoke's subnet, not just the hub's own subnet — packet source/destination IPs are unchanged by decryption, so the hub's ACLs must account for all traffic transiting that specific tunnel.
- **Packet Tracer limitation discovered**: crypto maps cannot be applied to an SVI backed by an EtherSwitch network module (`no switchport` is not supported on these simulated modules, unlike real Cisco hardware where this is a documented, supported workaround). Crypto maps require a native routed interface.
- **Decision**: the London branch was removed from the topology after confirming the concept was understood and the hardware limitation was hit. This limitation directly informed the correct approach taken later in this phase (see section 4) — using an `HWIC-1GE-SFP` module for genuine routed interfaces rather than an EtherSwitch module.

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

### 4. HSRP Gateway Redundancy (Both Sites) — Completed

**Toronto (YYZ-BR) and New York (NYC-HQ) — Full Build:**
- Added a second Layer 3 switch at each site (`YYZ-BR-CS-02`, `NYC-HQ-CS-02`), dual-homed to all existing access switches alongside the original core switch, plus a dedicated inter-switch link for HSRP hello exchange.
- Re-addressed every VLAN SVI with a dedicated real IP per switch (`.252`/`.253` convention), freeing the original gateway address on each VLAN to become the shared HSRP virtual IP — zero end-device reconfiguration required across either site.
- Implemented **HSRP load-sharing**: primary/Active role split across VLANs between the two switches at each site (rather than one switch sitting idle), with priority 105 configured on whichever switch is primary for a given VLAN, default 100 on the backup.
- Added a **second, independent physical uplink** from each site's CS-02 to its respective edge router (`HWIC-1GE-SFP` module + `GLC-LH-SMD` fiber transceiver, after discovering EtherSwitch modules cannot provide genuine routed interfaces — see section 1), giving each core switch a real, separate path to the WAN — a prerequisite for `standby track` to be functionally meaningful rather than cosmetic.
- Fully integrated both CS-02 switches into OSPF, with unique router-IDs (`5.5.5.5` for NYC-HQ-CS-02, `6.6.6.6` for YYZ-BR-CS-02) and `network` statements covering every real interface — verified systematically via `show ip interface brief` cross-checked against `show running-config | section router ospf` on every device, both routers and all four core switches.
- Configured `standby track` on each switch's own dedicated uplink interface, per VLAN it is primary on.
- **Key finding**: this platform's simulated IOS does not support a configurable `decrement` parameter on `standby track` (unlike real Cisco IOS) — it only accepts a bare `track <interface>` with an implicit default decrement of 10. Priority values were retuned (105/100 instead of the initially-planned 150/100) so the fixed default decrement would actually be sufficient to flip an election on failure.
- **Key finding**: `preempt` must be configured on **both** switches for every group, not just the switch intended as "primary." Preempt governs whether a switch is willing to seize Active status from a peer whose priority has become lower — a tracked-interface failure event requires the *backup* switch to have preempt configured too, or it will correctly see a lower-priority incumbent and still decline to take over.
- **Verified with a live, failure-triggered test** (not just a priority/preempt demonstration): shut down a tracked uplink interface, confirmed automatic failover to the peer switch, restored the interface, and confirmed automatic reclaim by the original primary switch via preempt — the full HSRP lifecycle observed end-to-end with real command output at every stage.
- **Troubleshooting note**: mid-build, HSRP unexpectedly failed to form peer relationships for a subset of VLANs despite correct configuration, healthy physical links, and correct STP forwarding state on all interfaces. Root cause was traced to accumulated Packet Tracer simulation-engine state corruption (not a configuration error) after an extended, heavily-modified session — resolved by a full topology power cycle. Config was saved before the reset, per the standing `write memory` / verification discipline established earlier in this phase.

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
| Dual-Homing Prerequisite | `standby track` only produces a meaningful failover if the tracking switch has its own independent physical path to the resource being tracked — without a second uplink, "failover" just relocates the same outage |
| Preempt Symmetry | `preempt` must be configured on every switch in a group, not just the intended primary — it governs willingness to seize Active status from any lower-priority incumbent, which the backup switch needs during a tracked-failure event, not just during its own post-crash recovery |
| Platform Decrement Limitation | This Packet Tracer IOS version only supports a fixed default `track` decrement (10) — priority spreads must be deliberately tuned to that fixed value rather than assumed configurable |
| OSPF Coverage Audit Method | For any device, cross-check every real IP in `show ip interface brief` against the device's own `network` statements — network statements from one device are never inherited by or relevant to another device's OSPF process |
| Simulation-State Corruption | Extended, heavily-modified Packet Tracer sessions can accumulate simulation-engine state issues that mimic real configuration bugs (e.g., asymmetric STP roles, HSRP peers going "unknown") — a full topology power cycle can resolve these when configuration has been independently verified correct |

---

## Redundancy — Phase 6 Status: ✅ Complete

Both Toronto and New York now have independently uplinked, load-shared, tracked, preempt-symmetric dual-core-switch HSRP redundancy, verified against a live, failure-triggered test rather than configuration inspection alone.

**Deferred to a future phase (not a current gap — a deliberate scope boundary):**
- Dual-homing the edge routers' own WAN/internet-facing links (the single remaining site-level point of failure)
- Extending `ip helper-address` / DHCP relay presence to CS-02 SVIs where not already covered
- Exploring SD-WAN concepts as the modern, software-managed evolution of the dual-path/multi-homing pattern built manually in this phase
