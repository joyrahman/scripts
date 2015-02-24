def list():
    curl -i $OS_STORAGE_URL -X GET -H "X-Auth-Token: $OS_AUTH_TOKEN"
