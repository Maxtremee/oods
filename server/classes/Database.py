from server.classes.Index import Index
from server.classes.Root import Root
import os
import pickle
import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s', datefmt='%d/%m/%Y %H:%M:%S')


def _check_if_db_exists(name):
    return os.path.isfile(f"{name}.db")


class Database:
    def create(name: str):
        """Creates database as a single file with .db extension
        
        If database with given name already exists it skips creation
        """
        if not _check_if_db_exists(name):
            root = Root()
            try:
                with open(f'{name}.db', 'wb') as file:
                    pickle.dump(root, file, protocol=pickle.HIGHEST_PROTOCOL)
                logging.info(f'Database \'{name}\' successfully created')
            except Exception as e:
                logging.error(e)
        else:
            logging.warn(
                f'Database \'{name}\' already exists. Skipping creation')

    def load(name: str) -> Root:
        """Loads database with given name"""
        root = None
        if _check_if_db_exists(name):
            with open(f'{name}.db', 'rb') as file:
                root = pickle.load(file)
            logging.info(f'Database \'{name}\' successfuly loaded')
            return root
        else:
            logging.error("No such database")

    def delete(name: str):
        """Deletes database with given name"""
        try:
            os.remove(f"{name}.db")
        except IOError as e:
            logging.error(e)

    def save(name: str, root: Root):
        """Saves database state to file"""
        with open(f'{name}.db', 'wb') as file:
            pickle.dump(root, file, protocol=pickle.HIGHEST_PROTOCOL)
