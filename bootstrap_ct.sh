# Takes vmid as first arg--which is $1 because this script is run with "bash"
# for ipa client interaction

# Try to read kerberos admin from environment, prompt otherwise
if [ -z ${KERBEROS_ADMIN+x} ]; then
	echo -n "FreeIPA user to join domain: "
	read kerberos_admin
else
	kerberos_admin=$KERBEROS_ADMIN
fi

pct list | grep -q $1 || exit
pct start $1 2> /dev/null

# Wait for IP address
while [ -z "$ip_addr" ]; do ip_addr="$(pct exec $1 -- hostname -I)"; done

# Get distro
release=$(pct exec $1 -- cat /etc/*-release)
if   echo $release | grep -q Ubuntu; then distro=ubuntu
	install_command='apt install -y'
	ipa_package='freeipa-client'
	pct exec $1 -- apt update
	pct exec $1 -- apt install -y python
elif echo $release | grep -q CentOS; then distro=centos
	install_command='yum install -y'
	ipa_package='ipa-client'
else >&2 echo "unknown distro; aborting" && exit
fi

# Install packages
install="$install_command $ipa_package openssh-server zsh"
install2=$(echo $install)
pct exec $1 -- $install2
pct exec $1 -- systemctl start sshd

# Ansible bootstrap
ansible_ct_id=108
pct exec $ansible_ct_id -- \
	ansible-playbook /root/craptops-ansible/baseline_servers.yml -i "$ip_addr",

# Enroll container in FreeIPA
pct exec $1 -- ipa-client-install --mkhomedir --enable-dns-updates --principal $kerberos_admin
