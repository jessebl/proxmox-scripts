#!/usr/bin/env python3
import argparse
from proxmoxer import ProxmoxAPI
import getpass

"""
General module for streamlined LXC creation.
Non-specific to any environment, aside from which options are supported.
"""

class LXC:

  available_templates = {
      'centos': 'local:vztmpl/centos-7-default_20170504_amd64.tar.xz',
      'debian': 'local:vztmpl/debian-9.0-standard_9.0-2_amd64.tar.gz',
      'fedora': 'local:vztmpl/fedora-27-default_20171212_amd64.tar.xz',
      'ubuntu': 'local:vztmpl/ubuntu-16.04-standard_16.04-1_amd64.tar.gz'
      }

  def __init__(self,
      hostname = None,
      node = 'localhost',
      ostemplate_type = 'centos',
      user = 'root@pam',
      storage = 'local-zfs',
      memory = 512,
      cores = 1,
      interface = 'name=eth0,bridge=vmbr0,firewall=0,ip=dhcp',
      keyfile = None,
      password = None,
      **kwargs):
    self.hostname = hostname
    self.node = node
    self.ostemplate_type = ostemplate_type
    self.user = user
    self.storage = storage
    self.memory = memory
    self.cores = cores
    self.interface = interface
    self.ostemplate = self.available_templates[self.ostemplate_type]
    self.password = password
    self.api = None
    self.vmid = None
    self.keyfile = keyfile
    self.pubkeys = self.read_keyfile()

  def read_keyfile(self):
    if self.keyfile:
      pubkeys = open(self.keyfile).read()
      return pubkeys

  def init_api(self):
    if not self.password:
      self.password = getpass.getpass(prompt = self.user + ':')
    self.api = ProxmoxAPI(self.node, user=self.user,
        password=self.password, verify_ssl=False)
    self.vmid = self.api.cluster.nextid.get()

  def create(self):
    if not self.api:
      self.init_api()
    ct_args = {"vmid": self.vmid,
        'ostemplate': self.ostemplate,
        'hostname': self.hostname,
        'storage': self.storage,
        'memory': self.memory,
        'cores': self.cores,
        'net0': self.interface,
        'ssh-public-keys': self.pubkeys}
    self.api.nodes(self.node).lxc.create(**ct_args)

def parse_args(parser):
  parser.add_argument('-l', '--list',
      help = 'list ostemplate-types',
      action = 'store_true')
  parser.add_argument('-H', '--hostname',
      help = 'container hostname',
      type = str)
  parser.add_argument('-n', '--node',
      help = 'Proxmox node for container',
      default = 'localhost',
      type = str)
  parser.add_argument('-o', '--ostemplate-type',
      help = 'container template type (distro)',
      default = 'centos',
      type = str)
  parser.add_argument('-u', '--user',
      help = 'Proxmox user@realm',
      default = 'root@pam',
      type = str)
  parser.add_argument('-s', '--storage',
      help = 'Proxmox node storage for container',
      default = 'local-zfs',
      type = str)
  parser.add_argument('-m', '--memory',
      help = 'container memory',
      default = 512,
      type = int)
  parser.add_argument('-c', '--cores',
      help = 'container number of cores',
      default = 1,
      type = int)
  parser.add_argument('-i', '--interface',
      help = 'container network interface config',
      default = 'name=eth0,bridge=vmbr0,firewall=0,ip=dhcp',
      type = str)
  parser.add_argument('-k', '--keyfile',
      help = 'SSH public key file (newline delimited)',
      type = str)
  args = parser.parse_args()
  return args

available_templates = {
  'centos': 'local:vztmpl/centos-7-default_20170504_amd64.tar.xz',
  'debian': 'local:vztmpl/debian-9.0-standard_9.0-2_amd64.tar.gz',
  'fedora': 'local:vztmpl/fedora-27-default_20171212_amd64.tar.xz',
  'ubuntu': 'local:vztmpl/ubuntu-16.04-standard_16.04-1_amd64.tar.gz'
  }

def list_templates():
  [print(key) for key in available_templates.keys()]

def main(**kwargs):
  parser = argparse.ArgumentParser(description='Create standard LXC container')
  args = parse_args(parser)
  ct_args = vars(args)
  ct = LXC(**ct_args)
  ct.create()
  print(ct.vmid)

if __name__ == '__main__':
  main()
