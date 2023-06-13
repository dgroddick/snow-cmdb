#!/usr/bin/env python

import os
import sys
import pprint
import argparse
from snow import Snow

sn_instance = os.getenv('SN_INSTANCE')
sn_user = os.getenv('SN_USERNAME')
sn_pw = os.getenv('SN_PASSWORD')
ci_table = 'cmdb_ci_linux_server'
path = '/table/' + ci_table


def main():
  parser = argparse.ArgumentParser()

  parser.add_argument('--debug')
  parser.add_argument('--debug-all', action='store_true')
  parser.add_argument('--add', action='store_true')
  parser.add_argument('--update', action='store_true')
  parser.add_argument('--delete')
  parser.add_argument('--delete-all', action='store_true')
  args = parser.parse_args()

  pp = pprint.PrettyPrinter(indent=4)
  now = Snow(sn_instance, sn_user, sn_pw, path)

  if args.debug:
    pp.pprint(now.get_host(args.debug))
  elif args.debug_all:
    pp.pprint(now.get_all_hosts()) 
  elif args.add: 
    folder = 'out'
    for filename in os.listdir(folder):
      f = os.path.join(folder, filename)
      if os.path.isfile(f):
        host = now.generate_ci_info(f)
        if host == "unreachable":
          print("{} is unreachable.".format(filename))
        else:
          now.add_host(host)
  elif args.update: 
    folder = 'out'
    for filename in os.listdir(folder):
      f = os.path.join(folder, filename)
      if os.path.isfile(f):
        host = now.generate_ci_info(f)
        if host == "unreachable":
          print("{} is unreachable.".format(filename))
        else:
          now.update_host(host)
  elif args.delete:
    now.delete_host(args.delete)
  elif args.delete_all:
    hosts = now.get_all_hosts()
    for host in hosts:
      for key in host.keys():
        now.delete_host(key)

if __name__ == '__main__':
  main()
