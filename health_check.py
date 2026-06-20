{
  "datacenter_site": "NYC-HQ",
  "vlan_id": 888,
  "subnet_mask": "255.255.255.0",
  "active_servers": [
    {
      "server_role": "Domain Name Resolution (DNS)",
      "hostname": "NYC-HQ-SRV-DNS",
      "ip_address": "10.20.88.1",
      "status": "active"
    },
    {
      "server_role": "Active Directory (AD)",
      "hostname": "NYC-HQ-SRV-AD",
      "ip_address": "10.20.88.2",
      "status": "active"
    },
    {
      "server_role": "Secure File Storage (FTP)",
      "hostname": "NYC-HQ-SRV-FILE",
      "ip_address": "10.20.88.3",
      "status": "degraded"
    }
  ]
}
