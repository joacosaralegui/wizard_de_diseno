from pymongo import MongoClient
mongo_url ='mongodb+srv://dbArquitectura:wizarddiseño@cluster0.owhd6.mongodb.net/ArquitecturaDataBase?retryWrites=true&w=majority'

client = MongoClient(mongo_url)
db = client.ArquitecturaDataBase

arquitecturas = db.arquitecturas

#insertar un solo doc
def save_arqui(id,arqui):
    # TODO: guardar lista de arquis, poner vacia en el setOnInsert, y desp en el set agregarla a la lista
    result = arquitecturas.update_one(
        {'id':id},
        {'$setOnInsert': {'id':id},
         '$set': {'arqui': arqui}},
         upsert=True)
    return result.modified_count

def load_arqui(id):
    # TODO: traer la lista y sacar la utima. Chequear si la lista esta vacia!! Devolver none
    return arquitecturas.find_one({'id':id})

def remove_arqui(id):
    # TODO: consultar si el id tiene una lista de arquis y no esta vacia, sacar la ultima
    return None

# TODO: descartar_arqui(id):
# tirar la ultima

if __name__=="__main__":
    arqui1 = {"x":1}
    arqui2 = {"y":2}

    id = 124214

    # Guarda la primera
    save_arqui(id, arqui1)
    # Deberia imprimir la de x=1
    print(load_arqui(id))
    # Guarda la segunda
    save_arqui(id, arqui2)
    # Deberia imporimir la de y=2
    print(load_arqui(id))
    # sacamos la ultima que tiene
    remove_arqui(id)
    # imprime x=1
    print(load_arqui(id))