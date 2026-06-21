import json

# Define the file paths
json_file_path = "migration_data.json"
output_file_path = "cisco_migration_commands.txt"

print("📖 Reading migration blueprint data from JSON file...")

try:
    # 1. Open and load the raw JSON data file into a Python dictionary object
    with open(json_file_path, "r") as file:
        migration_data = json.load(file)
    
    # 2. Extract the high-level device metadata parameters
    switch_name = migration_data.get("target_device")
    management_ip = migration_data.get("management_ip")
    vlan_list = migration_data.get("vlans_to_migrate", [])
    
    print(f"📦 Found migration profile for target device: {switch_name}")
    print(f"🔨 Programmatically generating Cisco IOS configuration lines...")
    
    # 3. Initialize an empty list to store our generated Cisco CLI strings
    cisco_commands = []
    
    # Add the base global setup commands to the list
    cisco_commands.append("configure terminal")
    cisco_commands.append(f"hostname {switch_name}")
    cisco_commands.append("!")
    
    # 4. The Core Loop: Iterate through each individual VLAN dictionary object one-by-one
    for vlan in vlan_list:
        v_id = vlan.get("vlan_id")
        v_name = vlan.get("name")
        svi_ip = vlan.get("svi_ip")
        mask = vlan.get("subnet_mask")
        
        # Programmatically construct the exact Layer 2 VLAN database commands
        cisco_commands.append(f"vlan {v_id}")
        cisco_commands.append(f" name {v_name}")
        cisco_commands.append(" exit")
        
        # Programmatically construct the exact Layer 3 SVI routing gateway commands
        cisco_commands.append(f"interface vlan {v_id}")
        cisco_commands.append(f" ip address {svi_ip} {mask}")
        cisco_commands.append(" no shutdown")
        cisco_commands.append(" exit")
        cisco_commands.append("!")

    cisco_commands.append("end")
    cisco_commands.append("write memory")
    
    # 5. Write the final accumulated list of Cisco commands out to a clean text file
    with open(output_file_path, "w") as output_file:
        for command in cisco_commands:
            output_file.write(command + "\n")
            
    print(f"✅ Success! Generated migration script saved to: {output_file_path}")

except Exception as err:
    print(f"❌ Script failed to execute: {err}")
