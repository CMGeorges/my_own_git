import hashlib
import os


GIT_DIR = '.ugit'

def init():
    # Create necessary directories for the repository
    # Créer les répertoires nécessaires pour le dépôt
    os.makedirs(GIT_DIR)
    os.makedirs(f'{GIT_DIR}/objects')


def hash_object(data, type_='blob'):
    # Compute the hash of the data and store it as an object
    # Calculer le hash des données et les stocker comme un objet
    obj = type_.encode() + b'\x00' + data
    oid = hashlib.sha1(obj).hexdigest()
    with open(f'{GIT_DIR}/objects/{oid}', 'wb') as out:
        out.write(obj)
        return oid


def get_object (oid, expected='blob'):
    # Retrieve the object by its ID
    # Récupérer l'objet par son ID
    with open (f'{GIT_DIR}/objects/{oid}', 'rb') as f:
         obj = f.read()

    type_, _, content = obj.partition(b'\x00')
    type_ = type_.decode()

    if expected is not None:
         assert type_ == expected, f'Expected {expected}, got {type_}'
    
    return content