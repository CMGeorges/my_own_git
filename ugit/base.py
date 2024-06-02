import os
from . import data

# Importation du module de données


def write_tree(directory='.'):
    # Recursively write the directory tree to the object store
    # Écrire récursivement l'arborescence du répertoire dans le stockage d'objets
    entries = []
    with os.scandir(directory) as it:
        for entry in it:
            full = f'{directory}/{entry.name}'
            if is_ignored(full):
                continue
            if entry.is_file(follow_symlinks=False):
                with open(full, 'rb') as f:
                    oid = data.hash_object(f.read())
            elif entry.is_dir(follow_symlinks=False):
                type_ = 'tree'
                oid = write_tree(full)
            entries.append((entry.name, oid, type_))

    tree = ''.join(f'{type_} {oid} {name}\n' for name, oid, type_ in sorted(entries))

    return data.hash_object(tree.encode(), 'tree')

def _iter_tree_entries(oid):
    # Iterate over tree entries given the object ID
    # Itérer sur les entrées de l'arbre en donnant l'ID de l'objet
    if not oid:
        return
    tree = data.get_object(oid, 'tree')
    for entry in tree.decode().splitlines():
        type_, oid, name = entry.split(' ', 2)
        yield type_, oid, name


def get_tree(oid , base_path= ''):
    # Get the tree structure recursively starting from the given object ID
    # Obtenir la structure de l'arbre de manière récursive en partant de l'ID de l'objet donné
    result = {}
    for type_, oid, name in _iter_tree_entries(oid):
        assert '/' not in name
        assert name not in ('..', '.')
        path = base_path + name
        if type_ == 'blob':
            result[path] = oid
        elif type_ == 'tree':
            result.update(get_tree(oid, f'{path}/'))
        else:
            assert False, f'Unkown tree entry {type_}'
    return result

def _empty_current_directory():
    # Empty the current directory
    # Vider le répertoire courant
    for root, dirnames, filenames in os.walk('.', topdown=False)
    for filename in filenames:
        path = os.path.relpath(f'{root}/{filename}')
        if is_ignored(path):
            continue
        try:
            os.rmdir(path)
        except (FileExistsError, OSError):
            #Deletion might fail if the directory contains ignored files,
            # so it's ok
            # Si le dossier contient des fichiers ignoré la suppression pourriat échouée
            pass

def read_tree(tree_oid):
    # Read the tree and populate the current directory with its contents
    # Lire l'arbre et remplir le répertoire courant avec son contenu
    _empty_current_directory()
    for path, oid in get_tree(tree_oid, base_path='./').items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(data.get_object(oid))

def commit(message):
    # Create a commit with the given message
    # Créer un commit avec le message donné
    commit = f'tree {write_tree()}\n'
    commit += '\n'
    commit += f'{message}\n'

    oid = data.hash_object(commit.encode(), 'commit')

    data.set_HEAD(oid)

    return oid        

def is_ignored(path):
    return '.ugit' in path.split('/')