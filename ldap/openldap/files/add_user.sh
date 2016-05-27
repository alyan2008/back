#!/bin/bash

MY_DOMAIN=$1
LDAP_SUFFIX=$(sed -e 's/^/dc=/' -e 's/\./,dc=/g' <<< $MY_DOMAIN)

UN='$2' CN='$3' SN='$4' MAIL='$5'
ldapadd -H ldapi:/// -x -w $6 -D "cn=root,$LDAP_SUFFIX" <<EOF
dn: uid=$UN,ou=people,$LDAP_SUFFIX
uid: $UN
objectClass: inetOrgPerson
cn: $CN
sn: $SN
mail: $MAIL
userPassword: $7
EOF
