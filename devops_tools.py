#!/usr/bin/python

import hashlib
from base64 import urlsafe_b64encode as encode
from base64 import urlsafe_b64decode as decode
import crypt, getpass
import getpass
import fileinput
import argparse
import sys
import os


parser = argparse.ArgumentParser()

parser.add_argument('--tools', type=str, choices=['zabbix', 'rancher', 'OpenLDAP', 'Logs_Monitoring', 'Atlassian'])
parser.add_argument('--agent', type=str, choices=['zabbix', 'rancher', 'FluentD', 'All'])
parser.add_argument('--server', type=str, required = True)
parser.add_argument('--domain', type=str, help='mydomain.com', required = True)
parser.add_argument('--stash_username', type=str, required = True)

args = parser.parse_args()

def replaceAll(file,searchExp,replaceExp):
    for line in fileinput.input(file, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)


def makeSecret(password):
    salt = os.urandom(4)
    h = hashlib.sha1(password)
    h.update(salt)
    return "{SSHA}" + encode(h.digest() + salt)

if args.tools == 'zabbix':
	os.system("cd /tmp/; git clone http://%s@stash.icekernel.com/scm/playb/ansible-docker-zabbix-server.git" % args.stash_username)
        zabbix_db_pass = getpass.getpass("Please enter new password for Zabbix-DB: ")
        replaceAll("/tmp/ansible-docker-zabbix-server/inventory.ini","ansible_ssh_host=","ansible_ssh_host=%s" % args.server)       
        replaceAll("/tmp/ansible-docker-zabbix-server/zabbix.yml","domain:","domain: %s" % args.domain)
        replaceAll("/tmp/ansible-docker-zabbix-server/zabbix.yml","zabbix_db_pass:","zabbix_db_pass: %s" % zabbix_db_pass)
        os.system("cd /tmp/ansible-docker-zabbix-server/; ANSIBLE_CONFIG=./ansible.cfg ansible-playbook -i inventory.ini zabbix.yml -vvv")

if args.tools == 'rancher':
	os.system("cd /tmp/; git clone http://%s@stash.icekernel.com/scm/playb/ansible-docker-rancher.git" % args.stash_username)
	replaceAll("/tmp/ansible-docker-rancher/inventory.ini","ansible_ssh_host=","ansible_ssh_host=%s" % args.server)
	replaceAll("/tmp/ansible-docker-rancher/rancher.yml","domain:","domain: %s" % args.domain)
        os.system("cd /tmp/ansible-docker-rancher/; ANSIBLE_CONFIG=./ansible.cfg ansible-playbook -i inventory.ini rancher.yml -vvv")

if args.tools == 'OpenLDAP':
	os.system("cd /tmp/; git clone http://%s@stash.icekernel.com/scm/playb/ansible-docker-openldap-phpldapadmin.git" % args.stash_username)
	PASSWD_ROOT = getpass.getpass("Please enter new password for LDAP root: ")
	PASSWD_USER = getpass.getpass("Please enter new password for test LDAP user: ")
	user_name = raw_input("Please enter the name of the test user: ")
        hashed_root_password = makeSecret(str(PASSWD_ROOT))
	hashed_user_password = makeSecret(str(PASSWD_USER))
	replaceAll("/tmp/ansible-docker-openldap-phpldapadmin/inventory.ini","ansible_ssh_host=","ansible_ssh_host=%s" % args.server)
	replaceAll("/tmp/ansible-docker-openldap-phpldapadmin/openldap.yml","domain:","domain: %s" % args.domain)
	replaceAll("/tmp/ansible-docker-openldap-phpldapadmin/openldap.yml","HASHED_PASSWD_ROOT:","HASHED_PASSWD_ROOT: \"%s\"" % hashed_root_password)
	replaceAll("/tmp/ansible-docker-openldap-phpldapadmin/openldap.yml","HASHED_PASSWD_USER:","HASHED_PASSWD_USER: \"%s\"" % hashed_user_password)
	replaceAll("/tmp/ansible-docker-openldap-phpldapadmin/openldap.yml","OPEN_PASSWD_ROOT:","OPEN_PASSWD_ROOT: \"%s\"" % PASSWD_ROOT)
	replaceAll("/tmp/ansible-docker-openldap-phpldapadmin/openldap.yml","ldapuser","%s" % user_name)
	os.system("cd /tmp/ansible-docker-openldap-phpldapadmin/; ANSIBLE_CONFIG=./ansible.cfg ansible-playbook -i inventory.ini openldap.yml -vvv")
	
if args.tools == 'Logs_Monitoring':
	os.system("cd /tmp/; git clone http://%s@stash.icekernel.com/scm/playb/ansible-docker-logs-monitoring.git" % args.stash_username)
	replaceAll("/tmp/ansible-docker-logs-monitoring/inventory.ini","ansible_ssh_host=","ansible_ssh_host=%s" % args.server)
	replaceAll("/tmp/ansible-docker-logs-monitoring/logs-monitoring.yml","domain:","domain: %s" % args.domain)	
	os.system("cd /tmp/ansible-docker-logs-monitoring/; ANSIBLE_CONFIG=./ansible.cfg ansible-playbook -i inventory.ini logs-monitoring.yml -vvv")

if args.tools == 'Atlassian':
        os.system("cd /tmp/; git clone http://%s@stash.icekernel.com/scm/playb/ansible-docker-atlassian.git" % args.stash_username)
        replaceAll("/tmp/ansible-docker-atlassian/inventory.ini","ansible_ssh_host=","ansible_ssh_host=%s" % args.server)
        os.system("cd /tmp/ansible-docker-atlassian/; ANSIBLE_CONFIG=./ansible.cfg ansible-playbook -i inventory.ini atlassian.yml -vvv")

if args.agent:
	os.system("cd /tmp/; git clone http://%s@stash.icekernel.com/scm/playb/ansible-docker-agents.git" % args.stash_username)
	replaceAll("/tmp/ansible-docker-agents/inventory.ini","ansible_ssh_host=","ansible_ssh_host=%s" % args.server)
	if args.agent == 'zabbix':
		zabbix_server = raw_input("IP address of your zabbix server: ")
		replaceAll("/tmp/ansible-docker-agents/agents.yml","zabbix_agent:","zabbix_agent: true")
		replaceAll("/tmp/ansible-docker-agents/agents.yml","zabbix_server:","zabbix_server: %s" % zabbix_server)
	if args.agent == 'rancher':
		rancher_server = raw_input("IP address of your rancher server: ")
                replaceAll("/tmp/ansible-docker-agents/agents.yml","rancher_agent:","rancher_agent: true")
		replaceAll("/tmp/ansible-docker-agents/agents.yml","rancher_server:","rancher_server: %s" % rancher_server)
	if args.agent == 'FluentD':
		fluentd_server = raw_input("IP address of your fluentd server: ")
                replaceAll("/tmp/ansible-docker-agents/agents.yml","fluentd_agent:","fluentd_agent: true")
		replaceAll("/tmp/ansible-docker-agents/agents.yml","fluentd_server:","fluentd_server: %s" % fluentd_server)
	if args.agent == 'All':
		zabbix_server = raw_input("IP address of your zabbix server: ")
		rancher_server = raw_input("IP address of your rancher server: ")
		fluentd_server = raw_input("IP address of your fluentd server: ")
		replaceAll("/tmp/ansible-docker-agents/agents.yml","zabbix_agent:","zabbix_agent: true")
		replaceAll("/tmp/ansible-docker-agents/agents.yml","rancher_agent:","rancher_agent: true")
		replaceAll("/tmp/ansible-docker-agents/agents.yml","fluentd_agent:","fluentd_agent: true")
		replaceAll("/tmp/ansible-docker-agents/agents.yml","zabbix_server:","zabbix_server: %s" % zabbix_server)
		replaceAll("/tmp/ansible-docker-agents/agents.yml","rancher_server:","rancher_server: %s" % rancher_server)
		replaceAll("/tmp/ansible-docker-agents/agents.yml","fluentd_server:","fluentd_server: %s" % fluentd_server)
	os.system("cd /tmp/ansible-docker-agents/; ANSIBLE_CONFIG=./ansible.cfg ansible-playbook -i inventory.ini agents.yml -vvv")


	
