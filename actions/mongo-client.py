from pymongo import MongoClient
mongo_url = 'mongodb+srv://mauroandres:wizarddiseño@clusterrasachatbot.o2vjo.mongodb.net/dbWizard?retryWrites=true&w=majority'

client = MongoClient(mongo_url)
db = client.dbWizard

print(db.list_collection_names())

conversation = db['conversations'].find_one()