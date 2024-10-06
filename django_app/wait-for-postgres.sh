RETRIES=3

until psql -h $ -U $POSTGRES_USER -d $POSTGRES_DB -p $POSTGRES_PORT -c "select 1" > /dev/null 2>&1 || [ $RETRIES -eq 0 ]; do
  echo "Waiting for postgres server, $RETRIES remaining attempts..."
  RETRIES=$((RETRIES - 1))
  sleep 1
done