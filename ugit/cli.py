import argparse
import os
import sys

from . import base
from . import data

def main():
    # Parse command-line arguments and execute the corresponding function
    # Analyser les arguments de la ligne de commande et exécuter la fonction correspondante
    args = parse_args()
    args.func(args)


def parse_args():
    # Create the argument parser
    # Créer l'analyseur d'arguments
    parser = argparse.ArgumentParser()

    commands = parser.add_subparsers(dest='command')
    commands.required = True

    # Define the 'init' command
    # Définir la commande 'init'
    init_parser = commands.add_parser('init')
    init_parser.set_defaults(func=init)

    # Define the 'hash-object' command
    # Définir la commande 'hash-object'
    hash_object_parser = commands.add_parser('hash-object')
    hash_object_parser.set_defaults(func=hash_object)
    hash_object_parser.add_argument('file')

    # Define the 'cat-file' command
    # Définir la commande 'cat-file'
    cat_file_parser = commands.add_parser ('cat-file')
    cat_file_parser.set_defaults (func=cat_file)
    cat_file_parser.add_argument ('object')

    write_tree_parser = commands.add_parser('write-tree')
    write_tree_parser.set_defaults(func=write_tree)

    return parser.parse_args()


def init(args):
    # Initialize the repository
    # Initialiser le dépôt
    data.init()
    print(f'Initialized empty ugit repository in {os.getcwd()}/{data.GIT_DIR}')


def hash_object(args):
    # Compute and print the hash of the file
    # Calculer et imprimer le hash du fichier
    with open(args.file, 'rb') as f:
        print(data.hash_object(f.read()))


def cat_file(args):
    # Display the content of the object
    # Afficher le contenu de l'objet
    sys.stdout.flush()
    sys.stdout.buffer.write(data.get_object(args.object, expected=None))

def write_tree(args):
    base.write_tree()

