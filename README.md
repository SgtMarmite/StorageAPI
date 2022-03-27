# StorageAPI
 Keboola Storage API client \n
 written in Python:3.10.4

# How to use with Docker:
```
git clone https://github.com/SgtMarmite/StorageAPI.git
cd StorageAPI
*provide valid token in /app/config.json
docker build . -t KeboolaAPIClient
docker create --name dummy KeboolaAPIClient
docker cp dummy:/app/parsed_result.csv  output/
```