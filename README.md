# oods

Object Oriented Database System - project made for bachelor thesis of Computer Science degree at Wroclaw University of Science and Technology. It consists of two modules: server and client written entirely in Python. Main idea of project is to simplify data fetching by utilizing Python's *pickle* module, which serializes native Python objects. Therefore it's possible to *just* fetch the object without object realtional mapping. For instructions look below.

## How to
Run server with database name as required argument. Optional arguments are server address, port, autosave cycle duration, logging level and maximum number of connected clients (check defaults by running server with ``--help`` flag). Server also requires all models (classes) to be declared in ``classes.py`` located at the same directory. All classes need to inherit from Persistent and need to call ``super().__init__()`` in their init function. 

### Accessible types
Accessible types are:
 - normal attribute
 - list
 - dictionary
 - tuple

Attributes starting with '_' (local private attributes) will NOT be processed. They will not be available to query.

Unsupported types:
 - set
 - functions
 - any type with custom access style

## Notes

### Python's recursion limit
Python's default recursion limit is 1000 therefore maximum object nest level is also 1000. Processing objects of type 'Persistent' uses recursion to determine attributes value.

