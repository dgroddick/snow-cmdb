import pysnow
import json

class Snow():
  def __init__(self, instance, username, password, path):
    self.instance = instance
    self.username = username
    self.password = password
    self.path = path

    c = pysnow.Client(instance=self.instance, user=self.username, password=self.password)
    self.cmdb = c.resource(api_path=self.path)

    
  def get_all_hosts(self):
    hosts = []
    separator: ''
    resp = self.cmdb.get(stream=True)
    for record in resp.all():
      hosts.append({record['name']: record['sys_id']})

    return hosts

  def get_host(self, name):
    resp = self.cmdb.get(query={'name': name}, stream=True)
    if resp._response.status_code == 200:
      result = resp.one_or_none()
      return result
    
  def get_sysid(self, hostname):
    host = self.get_host(hostname)
    if host is not None:
      return host['sys_id']
    else:
      return None

  def update_host(self, data):
    try:
      sys_id = self.get_sysid(data['name'])
      if sys_id is None:
        print("Host doesn't exist")
        exit()

      resp = self.cmdb.update(query={'sys_id': sys_id}, payload=data)
      if resp._response.status_code == 200:
        print("{}: Updated Successfully.".format(data['name']))
      else:
        print("Probably not a success")
    except KeyError as err:
      print(err)
    except TypeError as err:
      print(err)

  def add_host(self, data):
    try:
      host = self.get_host(data['name'])
      if host is not None:
        print("{} already exists.".format(data['name']))
      else:
        result = self.cmdb.create(payload=data)
        print("{} added successfully.".format(data['name']))
    except KeyError as err:
      print(err)
    except TypeError as err:
      print(err)

  def delete_host(self, host):
    sys_id = self.get_sysid(host)
    if sys_id is None:
      print("Host doesn't exist")
      exit()

    print("Deleting host: " + host + ", sys_id: " + sys_id)
    #ch = input("Are you sure? (y/n) ")
    ch = 'y'
    if ch == 'n' or ch == 'N':
      exit()
    elif ch == 'y' or ch == 'Y':
      resp = self.cmdb.delete(query={'sys_id': sys_id})
      print(resp)
    else:
      print("What?")

  def parse_group(self, groups):
    ''' Parse the groups and remove unwanted '''
    remove = ['OracleLinux-6','OracleLinux-7','OracleLinux-8',
              'VMware-guest','CentOS-6','CentOS-7']
    for rm in remove[:]:
      if rm in groups:
        groups.remove(rm)
    return groups
    
  def generate_ci_info(self, datafile):
    ''' Generate the CI info from Ansible facts into JSON '''
    ci = {}
    f = open(datafile)
    data = json.load(f)
    if 'unreachable' in data:
      return "unreachable"
    else:
      try:
        ci['name'] = data['ansible_facts']['ansible_hostname']
        ci['host_name'] = data['ansible_facts']['ansible_hostname']
        ci['fqdn'] = data['ansible_facts']['ansible_fqdn']
        ci['ip_address'] = data['ansible_facts']['ansible_default_ipv4']['address']
        ci['short_description'] = data['ansible_facts']['ansible_local']['system_info']['system_information']['system_info_note']
        if data['ansible_facts']['ansible_os_family'] == 'RedHat':
          ci['os'] = 'Linux Red Hat'
        else:
          ci['os'] = 'GNU/Linux'
        ci['os_version'] = data['ansible_facts']['ansible_distribution_version']
        g = self.parse_group(data['ansible_facts']['ansible_local']['system_info']['server']['ansible_groups'])
        ci['attributes'] = json.dumps(g)
      except KeyError as err:
        print(err)
      f.close()
    return ci
