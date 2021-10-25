import os
import pickle
import shutil

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
            curdir = os.curdir
            try:
                os.mkdir(name)
                os.chdir(name)
                try:
                    with open('root.pickle', 'wb') as file:
                        pickle.dump(
                            Root(), file, protocol=pickle.HIGHEST_PROTOCOL)
                except pickle.PickleError as e:
                    eprint(e, e)
            except OSError as e:
                eprint(e, "Cannot create directory, check your permissions!")
            finally:
                os.chdir(curdir)
        else:
            print("Database already exists!")

    def load(name) -> Root:
        if _check_if_db_exists(name):
            curdir = os.curdir
            try:
                os.chdir(name)
                try:
                    with open('root.pickle', 'rb') as file:
                        return pickle.load(file)
                except OSError as e:
                    eprint(e, "Error opening database file!")
                except pickle.PickleError as e:
                    eprint(e, "Error loading database!")
                except Exception as e:
                    eprint(e, e)
            except OSError as e:
                eprint(e, "Cannot change directory! Did you create such database?")
            finally:
                os.chdir(curdir)
        else:
            print("No such database!")

    def delete(name):
        if _check_if_db_exists(name):
            shutil.rmtree(name)
