#!/bin/sh

# Genera le chiavi VAPID
openssl ecparam -genkey -name prime256v1 -noout -out vapid_private.pem
openssl ec -in vapid_private.pem -pubout -out vapid_public.pem

# Converti le chiavi in Base64 URL-safe
PUBLIC_KEY=$(openssl ec -in vapid_private.pem -pubout -outform DER | tail -c 65 | base64 | tr -d '\n' | tr '/+' '_-' | sed -E 's/=+$//')
PRIVATE_KEY=$(openssl ec -in vapid_private.pem -outform DER | tail -c 32 | base64 | tr -d '\n' | tr '/+' '_-' | sed -E 's/=+$//')

# Scrivi le chiavi in un file .env (puoi anche usare altri metodi)
echo "VAPID_PUBLIC_KEY=${PUBLIC_KEY}" >> .env
echo "VAPID_PRIVATE_KEY=${PRIVATE_KEY}" >> .env