#!/bin/bash

MY_DOMAIN={{ domain }}
LDAP_SUFFIX=$(sed -e 's/^/dc=/' -e 's/\./,dc=/g' <<< $MY_DOMAIN)

ldapadd -H ldapi:/// -x -w {{ PASSWD_ROOT }} -D "cn=root,$LDAP_SUFFIX" <<EOF
dn: $LDAP_SUFFIX
objectClass: domain
dc: $(sed -e 's/,.*//' -e 's/dc=//' <<< $LDAP_SUFFIX)
EOF

ldapadd -H ldapi:/// -x -w {{ PASSWD_ROOT }} -D "cn=root,$LDAP_SUFFIX" <<EOF
dn: ou=people,$LDAP_SUFFIX
ou: people
description: All users.
objectClass: organizationalUnit
EOF
