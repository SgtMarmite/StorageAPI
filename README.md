# StorageAPI
 Keboola Storage API client

# How to use
```
git clone https://github.com/SgtMarmite/StorageAPI.git
cd StorageAPI
*provide valid token in /app/config.json
docker build . -t KeboolaAPIClient
docker create --name dummy KeboolaAPIClient
docker cp dummy:/app/parsed_result.csv  output/
```