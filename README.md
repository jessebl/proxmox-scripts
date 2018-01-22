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
./create_ct --hostname my_ct --keyfile ~/ansible_ssh.pub
```

### Requirements:

  - `proxmoxer` Python3 package (available through pip3)
