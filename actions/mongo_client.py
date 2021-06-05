from pymongo import MongoClient
mongo_url ='mongodb+srv://dbArquitectura:wizarddiseño@cluster0.owhd6.mongodb.net/ArquitecturaDataBase?retryWrites=true&w=majority'

client = MongoClient(mongo_url)
db = client.ArquitecturaDataBase

arquitecturas = db.arquitecturas

#insertar un solo doc
def save_arqui(id,arqui):
    # TODO: guardar com lista de arquis
    result = arquitecturas.update_one(
        {'id':id},
        {'$setOnInsert': {'id':id},
         '$set': {'arqui': arqui}},
         upsert=True)
    return result.modified_count

def load_arqui(id):
    # TODO: traer la ultimad e la lista
    return arquitecturas.find_one({'id':id})


# TODO: descartar_arqui(id):
# tirar la ultima