Contributions
==============

The project code is domiciled at the GitHub repo https://github.com/temmy222/PyTOUGHREACT 

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Contributing to the code would involve you following the below procedures to quickly get started

1. Clone the repo using preferred cloning method
2. Install the library to enable you able to use the test example using

```python
pip install -e .
```
3. Modify the code 
4. Tests are conducted with pytest and coverage reports are performed using pytest-cov. Install pytest and pytest-cov using the commands below
   
```python
pip install pytest
```

```python
pip install pytest-cov
```
5. Run tests:  Run the below command from the root folder to run the tests
   
```python
pytest
```

6. Flake8 is also used to ensure code readability. Install flake8 using 
   
```python
pip install flake8
```
and run flake8 using

```python
flake8 src
```

7. PEP8 Naming package is also used to ensure adherence to PEP8. Install pep8-naming using 
   
```python
pip install pep8-naming
```

8. Make a pull request after passing all tests
9. More information can be found in developer notes in the documentation - https://pytoughreact.readthedocs.io/en/master/developer.html 