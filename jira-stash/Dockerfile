FROM ansible/ubuntu14.04-ansible:stable

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
# Add playbooks to the Docker image
ADD ./ /opt/jira-stash
WORKDIR /opt/jira-stash

# Run Ansible to configure the Docker image
RUN ANSIBLE_CONFIG=./ansible.cfg ansible-playbook -i ./inventory.ini ./jira-stash.yml -vvvv

# Other Dockerfile directives are still valid
#EXPOSE 22 3000 80
#ENTRYPOINT ["/usr/local/bin/apachectl", "-DFOREGROUND"]
