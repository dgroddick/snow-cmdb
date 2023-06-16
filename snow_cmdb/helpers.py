import json

def parse_group(groups):
  remove = ['OracleLinux-6','OracleLinux-7','OracleLinux-8','VMware-guest', 'resources_private','resources_public','kvm-host','CentOS-6','CentOS-7']
  for rm in remove[:]:
    if rm in groups:
      groups.remove(rm)
  return groups
    
def generate_ci_info(datafile):
  ci = {}
  with open(datafile) as f:
    data = json.load(f)
    #print(data)
    if 'unreachable' in data:
      return 'unreachable'
    else:
      try:
        ci['name'] = data['ansible_facts']['ansible_hostname']
        ci['host_name'] = data['ansible_facts']['ansible_hostname']
        ci['fqdn'] = data['ansible_facts']['ansible_fqdn']
        ci['ip_address'] = data['ansible_facts']['ansible_default_ipv4']['address']
        ci['short_description'] = data['ansible_facts']['ansible_local']['system_info']['system_information']['system_info_note']
        ci['u_siem_role'] = data['ansible_facts']['ansible_local']['system_info']['system_information']['system_info_siem_role']
        ci['u_threat_class'] = data['ansible_facts']['ansible_local']['system_info']['security']['threat_class']
        ci['u_risk_classrisk_class'] = data['ansible_facts']['ansible_local']['system_info']['security']['risk_class']
        ci['cpu_count'] = data['ansible_facts']['ansible_processor_count']
        ci['cpu_cores_count'] = data['ansible_facts']['ansible_processor_cores']
        ci['cpu_type'] = data['ansible_facts']['ansible_processor'][2]
        ci['ram'] = data['ansible_facts']['ansible_memtotal_mb']
        ci['dns_domain'] = data['ansible_facts']['ansible_domain']
        ci['virtual'] = 'true'

        #ci['comments'] = data['ansible_facts']['ansible_local']['system_info']['system_information']['system_info_sysowner_note']

        ci['comments'] = ', '.join(data['ansible_facts']['ansible_local']['system_info']['system_information']['system_info_sysowner_emails'])

        # OS Family
        if data['ansible_facts']['ansible_os_family'] == 'RedHat':
          ci['os'] = 'Linux Red Hat'
        else:
          ci['os'] = 'GNU/Linux'

        ci['os_version'] = data['ansible_facts']['ansible_distribution_version']

        # Used for prod, dev, uat
        if data['ansible_facts']['ansible_local']['system_info']['server']['env_name'] == 'prod':
          ci['used_for'] = 'Production'
        elif data['ansible_facts']['ansible_local']['system_info']['server']['env_name'] == 'dev':
          ci['used_for'] = 'Development'
        else:
          ci['used_for'] = 'Test'

        # Ansible group
        g = parse_group(data['ansible_facts']['ansible_local']['system_info']['server']['ansible_groups'])
        ci['attributes'] = json.dumps(g)
      except KeyError as err:
        print(err)

  return ci
