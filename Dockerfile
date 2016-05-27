FROM ansible/ubuntu14.04-ansible:stable

# Add playbooks to the Docker image
ADD /opt/jira-stash /op/jira-stash
WORKDIR /opt/jira-stash

# Run Ansible to configure the Docker image
RUN ANSIBLE_CONFIG=./ansible.cfg ansible-playbook jira-stash.yml -l local

# Other Dockerfile directives are still valid
#EXPOSE 22 3000 80
#ENTRYPOINT ["/usr/local/bin/apachectl", "-DFOREGROUND"]
