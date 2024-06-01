import os
from . import data

# Importation du module de données


def write_tree(directory='.'):
    # Recursively write the directory tree to the object store
    # Écrire récursivement l'arborescence du répertoire dans le stockage d'objets
    with os.scandir(directory) as it:
        for entry in it:
            full = f'{directory}/{entry.name}'
            if is_ignored(full):
                continue
            if entry.is_file(follow_symlinks=False):
                with open(full, 'rb') as f:
                    print(data.hash_object(f.read()), full)
            elif entry.is_dir(follow_symlinks=False):
                write_tree(full)

    #TODO actually create the tree object

def is_ignored(path):
    return '.ugit' in path.split('/')