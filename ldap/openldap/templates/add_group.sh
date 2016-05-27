#!/bin/bash

MY_DOMAIN={{ domain }}
LDAP_SUFFIX=$(sed -e 's/^/dc=/' -e 's/\./,dc=/g' <<< $MY_DOMAIN)

ldapadd -H ldapi:/// -x -w {{ PASSWD_ROOT }} -D "cn=root,$LDAP_SUFFIX" <<EOF
dn: ou=groups,$LDAP_SUFFIX
ou: groups
description: All groups.
objectClass: organizationalUnit
EOF
