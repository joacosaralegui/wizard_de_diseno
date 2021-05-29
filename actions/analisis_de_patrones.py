from rasa.nlu.model import Interpreter

# path of your model
rasa_model_path = "actions/models/patrones/nlu"

# create an interpreter object
interpreter = Interpreter.load(rasa_model_path)

"""
Function to get model output
Args:
  text  (string)  --  input text string to be passed)
For example: if you are interested in entities, you can just write result['entities']
Returns:
  json  --  json output to used for accessing model output
"""

def rasa_output(text):
    """
    Analisis NLU del texto para clasificar categorias de patrones:
    usa modelo de -> (https://github.com/joacosaralegui/analisis-de-patrones)
    """
    message = str(text).strip()
    result = interpreter.parse(message)
    return result

def get_categoria(text):
  """
  Saca solo el intent del análisis NLU
  """
  out = rasa_output(text)
  return out['intent']['name']

def get_recomendacion(text):
  """
  Dado un problema sugiere un patrón
  """
  categoria = get_categoria(text)
  return conocimiento[categoria]

conocimiento = {
  "ecommerce": "y, las aplicaciones así tipo e-commerce son complicadas. Yo te recomiendo un diseño de capaz donde podes tener la capa inicial de persistencia (ahi te guardas la info de los usuarios y los productos y todo eso) y despues arriba lógica del negocio, donde manejas las transacciones y las representaciones de operaciones, despues una de aplicacion donde tenes los servicios y funcionalidades y por ultimo la de presentacion que le pones toda la interfaz de usuario. Depende el lenguaje hay mil frameworks que podes usar. Y quizas hasta tambien algo tipo Model-View-Controller te viene bien.",
  "aplicaciones_online": "Mira, para las apliciones online como esta te recomiendo un patrón cliente servidor, que te va a venir bien para manejar toda la infomación importante en el server y a los clientes solo les proporcionas una vista y la posibilidad de hacer solicitudes.",
}