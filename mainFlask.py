from flask import Flask
#pip install -U flask-cors

from data.database import Database
#from pathlib import Path
import os
class MainFlask:
    """
    Clase donde se inicializa flask y la base de datos
    """
    app=None
    database=None

    @classmethod
    def getFlask(cls):
        """
        Método de clase que
        inicializa flask si no está inicializado

        Agrs:
            atributos estáticos
        """
        if cls.app is None:
            #THIS_FOLDER = Path(__file__).parent.resolve()
            #static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
            #static_folder =str(THIS_FOLDER)+"/static"
            #template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
            #template_folder = str(THIS_FOLDER)+"/templates"
            static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
            template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
            print("la ruta de los archivos estaticos es: ", static_folder)

            cls.app = Flask(__name__ , static_folder=static_folder,template_folder=template_folder)
            #cls.app = Flask(__file__)
            cls.app.secret_key = "mi secret key"
        return cls.app

    @classmethod
    def get_database(cls):
        """
        Método de clase que inicializa la base de datos si no está inicializada
        
        Args:
            Atributos estáticos
        """
        if cls.database is None:
            cls.database = Database()
        return cls.database


