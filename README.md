# Proxmox Scripts

Scripts for ease-of-use in Proxmox

## create_ct.py

Allows creation of an LXC container on a Proxmox node via the Proxmox API.
Can be used as a Python library or be called on the command-line with args
(see `create_ct.py --help` for help.

### Example usage

In Python:

```python
import create_ct
ct = create_ct.LXC(hostname='my_ct', keyfile='~/ansible_ssh.pub')
ct.create()
```

On the command line:

```bash
./create_ct.py --hostname my_ct --keyfile ~/ansible_ssh.pub
```

### Requirements:

  - `proxmoxer` Python3 package (available through pip3)

## bootstrap_ct.sh

Install some basic packages (including ssh server) and enroll container in
FreeIPA domain, also configuring it with an Ansible playbook. Can only be run
from a Proxmox node.

Script requires a Kerberos principal which is authorized to enroll hosts in
FreeIPA. The principal will be read from the `KERBEROS_ADMIN` environment variable if it exists, or from a user prompt if not.

### Example usage

```bash
# Where <vmid> is the ID of the container to be configured
./bootstrap_ct.sh <vmid>
```

## restart_lxc.sh

Simply restarts all containers running on the Proxmox node.
