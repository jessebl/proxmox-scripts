#!/usr/bin/env python3
import argparse
from proxmoxer import ProxmoxAPI
import getpass

"""
General module for streamlined LXC creation.
Non-specific to any environment, aside from which options are supported.
"""

parser = argparse.ArgumentParser(description='Create standard LXC container')
parser.add_argument('-N', '--node',
    help = 'Proxmox node on which to create the container',
    type = str,
    default = 'localhost')
parser.add_argument('-l',
    '--list-templates',
    help = 'list available templates',
    action ='store_true')
parser.add_argument('-t',
    '--template',
    help = 'template to user for container',
    type = str,
    default = 'centos')
parser.add_argument('-n', '--name',
    help = 'hostname for container',
    type = str)
parser.add_argument('-u', '--user',
    help = 'proxmox user (user@realm)',
    type = str,
    default = 'root@pam')
parser.add_argument('-s', '--storage',
    help = 'storage for container',
    type = str,
    default = 'local-zfs')
parser.add_argument('-m', '--memory',
    help = 'memory for container',
    type = int,
    default = 512)
parser.add_argument('-c', '--cores',
    help = 'number of cores for container',
    type = int,
    default = 1)
parser.add_argument('-i', '--interface',
    help = 'network interface for container',
    type = str,
    default = 'name=eth0,bridge=vmbr0,firewall=0,ip=dhcp')
parser.add_argument('-o', '--onboot',
    help = 'start container at boot',
    type = int,
    default = 1)
parser.add_argument('-p', '--password',
    help = 'Proxmox API password',
    type = str)
parser.add_argument('-V', '--vmid',
    help = 'Container VMID',
    type = int)
parser.add_argument('-P', '--pubkey',
    help = 'public key string for container',
    type = str)
args = parser.parse_args()

available_templates = {
  'centos': 'local:vztmpl/centos-7-default_20170504_amd64.tar.xz',
  'debian': 'local:vztmpl/debian-9.0-standard_9.0-2_amd64.tar.gz',
  'fedora': 'local:vztmpl/fedora-27-default_20171212_amd64.tar.xz',
  'ubuntu': 'local:vztmpl/ubuntu-16.04-standard_16.04-1_amd64.tar.gz'
  }

def list_templates():
  [print(key) for key in available_templates.keys()]

def create_ct(node):
  """Takes Proxmoxer node object and creates container on it"""
  ct_args = {"vmid": args.vmid,
      'ostemplate': available_templates[args.template],
      'hostname': args.name,
      'storage': args.storage,
      'memory': args.memory,
      'cores': args.cores,
      'net0': args.interface,
      'ssh-public-keys': args.pubkey}
  node.lxc.create(**ct_args)
  print(args.vmid)

def main():
  if args.list_templates:
    list_templates()
  elif args.template and args.name:
    if not args.password:
      args.password = getpass.getpass(prompt = args.user + ':')
    api = ProxmoxAPI(args.node, user=args.user,
        password=args.password, verify_ssl=False)
    if not args.vmid:
      args.vmid = api.cluster.nextid.get()
    node = api.nodes(args.node)
    create_ct(node)

if __name__ == '__main__':
  main()
