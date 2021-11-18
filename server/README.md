# oods server

Object Oriented Database System - project made for bachelor thesis of Computer Science degree at Wroclaw University of Science and Technology. It consists of two modules: server and client written entirely in Python. Main idea of project is to simplify data fetching by utilizing Python's *pickle* module, which serializes native Python objects. Therefore it's possible to *just* fetch the object without object realtional mapping. For instructions look below.

## How to
Attributes starting with '_' (local private attributes) will NOT be processed. They will not be available to query.

### Accessible types
Accessible types are:
 - normal attribute
 - list
 - dictionary
 - tuple

Unsupported types:
 - set
 - functions
 - any type with custom access style

## Notes

### Python's recursion limit
Python's default recursion limit is 1000 therefore maximum object nest level is also 1000. Processing objects of type 'Persistent' uses recursion to determine attributes value.

