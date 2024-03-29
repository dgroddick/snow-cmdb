import os
import sys
import pprint
import argparse

from .snow import Snow
from .helpers import *

sn_instance = os.getenv('SN_INSTANCE')
sn_user = os.getenv('SN_USERNAME')
sn_pw = os.getenv('SN_PASSWORD')
ci_table = 'cmdb_ci_linux_server'
path = '/table/' + ci_table


def main():
  parser = argparse.ArgumentParser(description='A tool to manage Ansible hosts in the ServiceNow CMDB.')

  parser.add_argument('-o', '--output', help='Print out CI data for a single host')
  parser.add_argument('--output-all', action='store_true', help='Print out all hosts in CMDB')
  parser.add_argument('-a', '--add', action='store_true', help='Add hosts to CMDB')
  parser.add_argument('-u', '--update', action='store_true', help='Update hosts in CMDB')
  parser.add_argument('-d', '--delete', help='Delete a host from the CMDB')
  parser.add_argument('--delete-all', action='store_true', help='Delete all hosts from the CMDB')
  args = parser.parse_args()

  pp = pprint.PrettyPrinter(indent=4)
  now = Snow(sn_instance, sn_user, sn_pw, path)

  if args.output:
    # Dump out SN info for single host
    pp.pprint(now.get_host(args.output))

  elif args.output_all:
    # Dump hostname and sys_id for all hosts in CMDB
    pp.pprint(now.get_all_hosts())

  elif args.add:
    # Add new host into CMDB
    folder = 'out'
    for filename in os.listdir(folder):
      f = os.path.join(folder, filename)
      print("-- Opening {}".format(filename))
      if os.path.isfile(f):
        host = generate_ci_info(f)
        if "unreachable" in host:
          print("{} is unreachable.".format(filename))
        else:
          now.add_host(host)

  elif args.update: 
    # Update existing host in CMDB
    folder = 'out'
    for filename in os.listdir(folder):
      f = os.path.join(folder, filename)
      if os.path.isfile(f):
        host = generate_ci_info(f)
        if "unreachable" in host:
          print("{} is unreachable.".format(filename))
        else:
          now.update_host(host)

  elif args.delete:
    # Delete single host from CMDB
    now.delete_host(args.delete)

  elif args.delete_all:
    # Delete all hosts in CMDB
    hosts = now.get_all_hosts()
    for host in hosts:
      for key in host.keys():
        now.delete_host(key)

if __name__ == '__main__':
  main()
