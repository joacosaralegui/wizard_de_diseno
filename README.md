# wizard_de_diseno
Chatbot especializado en diseño de software desarrollado con Rasa

## Instalación
Instalar Python 3.7, pip y virtualenv y crear un nuevo virtual enviroment: <br/>
https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

Para python 3.7
```
sudo apt-get install python3.7
sudo apt-get install python3.7-dev
virtualenv env -p python3.7
```


Con el virtual env activado, instalar los requerimientos corriendo<br/>
```pip install -r requirements.txt```

### Windows (si no queda otra)
https://www.youtube.com/watch?v=GlR60CvTh8A&ab_channel=Rasa

## Desarrollo

Las principales modificaciones se realizan en los archivos de nlu (carpeta data) con en los de dominio (domain.yml)

Para desarrollar se usan los comandos:<br/>
`rasa train` para entrenar el modelo luego de hacer modificaciones <br/>
`rasa shell` para probar el chatbot en la consola<br/>
`rasa interactive` para guiar al chatbot de manera interactiva y aplicar correcciones<br/>

## Deploy
`rasa n -m models --enable-api --cors "*" --debug`
