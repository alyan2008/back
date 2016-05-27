#!/bin/bash

ldapmodify -H ldapi:/// <<EOF
dn: olcDatabase={2}hdb,cn=config
changetype: modify
add: olcRootPW
olcRootPW: $1
EOF
