# Tests folder

To run tests, install the re queirements and run

```bash
~$ export PYTHONPATH=$PYTHONPATH:$PWD/src:$PWD/tests
~$ python -m unittest discover ./tests
```

To run specific types of tests, for example unit test run

```bash
~$ export PYTHONPATH=$PYTHONPATH:$PWD/src:$PWD/tests
~$ python -m unittest discover ./tests/unit
```
