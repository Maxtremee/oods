# oods

## How to
Maximum python version is 3.8.12.
Attributes starting with '_' (local private attributes) will NOT be processed. They will not be available to query.

## Notes

### Python's recursion limit
Python's default recursion limit is 1000 therefore maximum object nest level is also 1000. Processing objects of type 'Persistent' uses recursion to determine attributes' paths.

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