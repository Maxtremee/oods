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


# class Database:
#     def create(name):
#         if not _check_if_db_exists(name):
#             try:
#                 os.mkdir(name)
#                 try:
#                     with open(f'{name}/root.pickle', 'wb') as file:
#                         pickle.dump(
#                             Root(), file, protocol=pickle.HIGHEST_PROTOCOL)
#                 except pickle.PickleError as e:
#                     eprint(e, e)
#             except OSError as e:
#                 eprint(e, "Cannot create directory, check your permissions!")
#         else:
#             print("Database already exists! Skipping")

#     def load(name) -> Root:
#         while not _check_if_db_exists(name):
#             time.sleep(0.0001)

#         if _check_if_db_exists(name):
#             try:
#                 with open(f'{name}/root.pickle', 'rb') as file:
#                     return pickle.load(file)
#             except OSError as e:
#                 eprint(e, "Error opening database file!")
#             except pickle.PickleError as e:
#                 eprint(e, "Error loading database!")
#             except Exception as e:
#                 eprint(e, e)
#             except OSError as e:
#                 eprint(e, "Cannot change directory! Did you create such database?")
#         else:
#             raise ValueError("No such database!")

#     def delete(name):
#         if _check_if_db_exists(name):
#             shutil.rmtree(name)
#         else:
#             raise ValueError("No such database!")
