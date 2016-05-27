#!/bin/bash

MY_DOMAIN={{ domain }}
LDAP_SUFFIX=$(sed -e 's/^/dc=/' -e 's/\./,dc=/g' <<< $MY_DOMAIN)
ldapmodify -H ldapi:/// <<EOF
dn: olcDatabase={2}hdb,cn=config
changetype: modify
replace: olcSuffix
olcSuffix: $LDAP_SUFFIX

dn: olcDatabase={2}hdb,cn=config
changetype: modify
replace: olcRootDN
olcRootDN: cn=root,$LDAP_SUFFIX

EOF
