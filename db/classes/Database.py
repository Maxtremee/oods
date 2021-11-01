import os
import pickle
import shutil
import time

from db.classes.Root import Root
from db.misc.eprint import eprint


def _check_if_db_exists(name):
    is_dir = os.path.isdir(name)
    has_root = os.path.isfile(f"{name}/root.pickle")
    if not is_dir:
        return False
    if not has_root:
        return False
    return True


class Database:
    def create(name):
        if not _check_if_db_exists(name):
            try:
                os.mkdir(name)
                try:
                    with open(f'{name}/root.pickle', 'wb') as file:
                        pickle.dump(
                            Root(), file, protocol=pickle.HIGHEST_PROTOCOL)
                except pickle.PickleError as e:
                    eprint(e, e)
            except OSError as e:
                eprint(e, "Cannot create directory, check your permissions!")
        else:
            print("Database already exists! Skipping")

    def load(name) -> Root:
        while not _check_if_db_exists(name):
            time.sleep(0.0001)

        if _check_if_db_exists(name):
            try:
                with open(f'{name}/root.pickle', 'rb') as file:
                    return pickle.load(file)
            except OSError as e:
                eprint(e, "Error opening database file!")
            except pickle.PickleError as e:
                eprint(e, "Error loading database!")
            except Exception as e:
                eprint(e, e)
            except OSError as e:
                eprint(e, "Cannot change directory! Did you create such database?")
        else:
            raise ValueError("No such database!")

    def delete(name):
        if _check_if_db_exists(name):
            shutil.rmtree(name)
        else:
            raise ValueError("No such database!")
