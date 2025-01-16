"""Make SQLite database from novelWriter GUI translation file.

Output:
    - SQLite database nw_gui_dict.db.
        Tables:
            nw_context(id, name)
            nw_translation(id, fk_context, source, translation)
Usage:
    ts_to_sqlite.py sourcefile.ts
"""
__version__ = "0.1"
__author__ = "Jean-Michel Heras"

import xml.etree.ElementTree as ET
import sqlite3

from argparse import ArgumentParser

def parse_arguments():
    """Get argument command line. """
    parser = ArgumentParser()

    parser.add_argument(dest="translation_file", type=str,
                        help="Enter file name")


    input_args = parser.parse_args()
    file = input_args.translation_file
    return file


def create_base(data_base):
    """ Create SQLite database from nw_xx_XX.ts file."""

    try:
        with sqlite3.connect(data_base, autocommit=False) as connection:
            # Auto-validation disabled (recommended for Python 3.12 and later)
            cursor = connection.cursor()
            cursor.execute("DROP TABLE IF EXISTS nw_translation")
            cursor.execute("DROP TABLE IF EXISTS nw_context")
            cursor.execute("PRAGMA foreign_keys = ON") # Activate foreign keys
            # Execute script
            cursor.executescript("""
                CREATE TABLE nw_context(
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                name TEXT UNIQUE);

                CREATE TABLE nw_translation(
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                fk_context INTEGER,
                source TEXT,
                translation TEXT,
                FOREIGN KEY (fk_context) REFERENCES nw_context(id))
                """)

            connection.commit()
        connection.close()

    except sqlite3.Error as e:
        print(e.sqlite_errorcode,  e.sqlite_errorname)


def fill_nw_context(data_base, name):
    """ Fill nw_context table with context name"""

    try:
        with sqlite3.connect(data_base, autocommit=False) as connexion:
            # Auto-validation disabled (recommended for Python 3.12 and later)
            curseur = connexion.cursor()
            curseur.execute("PRAGMA foreign_keys = ON") # Activate foreign keys

            # EWrite in nw_context table
            curseur.executemany("INSERT INTO nw_context (name) VALUES (?)", name)

            connexion.commit()
        connexion.close()

    except sqlite3.Error as e:
        print(e.sqlite_errorcode,  e.sqlite_errorname)


def fill_nw_translation(data_base, translation):
    """ Fill nw_translation with context foreign key,
    source & translation strings.
    
    """
    
    try:
        with sqlite3.connect(data_base, autocommit=False) as connexion:
            # Auto-validation disabled (recommended for Python 3.12 and later)
            curseur = connexion.cursor()
            curseur.execute("PRAGMA foreign_keys = ON") # Activate foreign keys

            # Write in nw_translation table
            curseur.executemany("INSERT INTO nw_translation (fk_context, source, translation) VALUES (?, ?, ?)", translation)

            connexion.commit()
        connexion.close()

    except sqlite3.Error as e:
        print(e.sqlite_errorcode,  e.sqlite_errorname)


def list_from_nw_context(data_base):
    """ Make a list of tuple with (id, name) from nw_context table.
    
    Manage foreign keys.
    """

    try:
        with sqlite3.connect(data_base, autocommit=False) as connexion:
            # Auto-validation désactivée (recommandé à partir de Python 3.12)
            # connexion.row_factory = sqlite3.Row
            curseur = connexion.cursor()
            curseur.execute("PRAGMA foreign_keys = ON") # Active les clés étrangères

            # Select * from table nw_context
            curseur.execute("SELECT * FROM nw_context")

            result = curseur.fetchall()
        connexion.close()
        return result

    except sqlite3.Error as e:
        print(e.sqlite_errorcode,  e.sqlite_errorname)


def get_xmlroot(file):
    """Get root tree of xml file."""
    
    try:
        tree = ET.parse(file)
        root = tree.getroot()
    except FileNotFoundError:
        print("File not found!")
        quit()
    else:
        return root


def get_context_name(root):
    """Get name of context.

    Make list of tuples with context name.
    """
    context_data = [(context.find('name').text,) for context in root.findall('context')]
    return context_data


def make_translation_tuple(data_base, context_list, root):
    """ Make list of tuple forein_key, source, translation for one context.
 
    Loop on context list to get id and give foreign key.
    Get source and translation.
    Then send to fill translation table.
    """
    for item in context_list:
        id_context, name_context = item
        source = [s_name.text for s_name in root.findall(".//context[name='%s']/message/source" % name_context)]
        translation = [t_name.text for t_name in root.findall(".//context[name='%s']/message/translation" % name_context)]
        foreign_keys = [id_context] * len(source)

        translation_list = list(zip(foreign_keys, source, translation))
        fill_nw_translation(data_base, translation_list)


def main():
    # Parse argument.
    file = parse_arguments()

    # Create database.
    data_base = "nw_gui_dict.db"

    create_base(data_base)

    # Get xlm root tree.
    root = get_xmlroot(file)

    # Get context name.
    context_name = get_context_name(root)

    # Fill nw_context table with name.
    fill_nw_context(data_base, context_name)

    # Make list of tuple from nw_context to manage foreign keys
    context_list = list_from_nw_context(data_base)

    # Fill nw_translation table with source and translation.
    make_translation_tuple(data_base, context_list, root)


if __name__ == "__main__":
    main()

