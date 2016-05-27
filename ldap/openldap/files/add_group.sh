#!/bin/bash

MY_DOMAIN=$1
LDAP_SUFFIX=$(sed -e 's/^/dc=/' -e 's/\./,dc=/g' <<< $MY_DOMAIN)

ldapadd -H ldapi:/// -x -w $2 -D "cn=root,$LDAP_SUFFIX" <<EOF
dn: ou=groups,$LDAP_SUFFIX
ou: groups
description: All groups.
objectClass: organizationalUnit
EOF
