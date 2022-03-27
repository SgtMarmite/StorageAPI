# StorageAPI
 Keboola Storage API task

# How to use
'''
git clone https://github.com/SgtMarmite/StorageAPI.git
cd StorageAPI
*rename dummy_config.json to config.json and provide valid token 
docker build . -t keboola
docker create --name dummy keboola
docker cp dummy:/app/parsed_result.csv  output/
'''