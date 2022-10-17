#!/usr/bin/env python

import os
import sys
import pprint

from snow import Snow

sn_instance = 'unedev'
sn_user = os.getenv('SN_USERNAME')
sn_pw = os.getenv('SN_PASSWORD')
ci_table = 'cmdb_ci_linux_server'
path = '/table/' + ci_table


def main():
  pp = pprint.PrettyPrinter(indent=4)
  now = Snow(sn_instance, sn_user, sn_pw, path)
  #pp.pprint(hosts)
   
  #hosts = now.get_all_hosts()
  #for host in hosts:
  #  for key in host.keys():
  #    now.delete_host(key)

  folder = 'out'
  for filename in os.listdir(folder):
    f = os.path.join(folder, filename)
    if os.path.isfile(f):
      host = now.generate_ci_info(f)
      now.add_host(host)

if __name__ == '__main__':
  main()
