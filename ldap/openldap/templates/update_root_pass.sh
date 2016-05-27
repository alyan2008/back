#!/bin/bash

ldapmodify -H ldapi:/// <<EOF
dn: olcDatabase={2}hdb,cn=config
changetype: modify
add: olcRootPW
olcRootPW: {{ HASHED_PASSWD_ROOT }}
EOF
