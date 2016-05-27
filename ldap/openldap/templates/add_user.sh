#!/bin/bash

MY_DOMAIN={{ domain }}
LDAP_SUFFIX=$(sed -e 's/^/dc=/' -e 's/\./,dc=/g' <<< $MY_DOMAIN)

UN={{ username }} CN={{ fullname }} SN={{ surname }} MAIL={{ email }} PASS={{HASHED_PASSWD_USER}}
ldapadd -H ldapi:/// -x -w {{ PASSWD_ROOT }} -D "cn=root,$LDAP_SUFFIX" <<EOF
dn: uid=$UN,ou=people,$LDAP_SUFFIX
uid: $UN
objectClass: inetOrgPerson
cn: $CN
sn: $SN
mail: $MAIL
userPassword: $PASS
EOF
