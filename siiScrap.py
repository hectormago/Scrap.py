# Made with love by Karlpy
import requests
import pymongo
from pymongo import MongoClient
from dataclasses import dataclass
from lxml import etree
from io import StringIO

siis_url = 'https://sistema.siis.gov.py/fuentes_externas/legajo_participante.php?p_documento='

# Cedula (id) range
start = 3000260
stop = 3000370

cedula_generator = (i for i in range(start, stop + 1))

client = MongoClient()
db = client.siis
collection = db.siis_data

@dataclass
class DatosPersona:
    apellido: str
    nombre: str
    nro_documento: str
    sexo: str
    nacionalidad: str
    lugar_de_nacimiento: str
    fecha_nacimiento: str
    edad: int

session = requests.Session()
parser = etree.HTMLParser()

for ced in cedula_generator:
    try:
        req_url = f'{siis_url}{ced}'
        req = session.get(req_url)
        html = req.content.decode("utf-8")
        tree = etree.parse(StringIO(html), parser=parser)
        
        apellido = tree.find('//*[@id="e_apellido"]').attrib['value']
        nombre = tree.find('//*[@id="e_nombre"]').attrib['value']
        nro_documento = tree.find('//*[@id="e_documento"]').attrib['value']
        sexo = tree.find('//*[@id="e_sexo"]').attrib['value']
        nacionalidad = tree.find('//*[@id="e_nacionalidad"]').attrib['value']
        lugar_de_nacimiento = tree.find('//*[@id="e_lugar"]').attrib['value']
        fecha_nacimiento = tree.find('//*[@id="e_fec_nac"]').attrib['value']
        edad = tree.find('//*[@id="e_edad"]').attrib['value']

        persona = DatosPersona(apellido, nombre, nro_documento, sexo, nacionalidad, lugar_de_nacimiento, fecha_nacimiento, edad)
        if persona.apellido != None:
            print('add to mongodb')
            print(persona)


    except Exception as e:
        print(e)
        continue