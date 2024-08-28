# InfraTools

## Venv config
### Create
```sh
python -m venv /path/to/new/virtual/environment/infra_tools
```
### Active
```sh
source /path/to/new/virtual/environment/infra_tools/bin/active
```

## Install Dependencies 
```sh
pip install pyside6 self socket re uuid
```

## Create config.ini
The config.ini define the hosts and domain. Exemple:

[hosts] are advised to be internal links to Microsoft AD or equivalent 

[domain] is internal domain

```ini
[hosts]
ips = 1.1.1.1, 1.0.0.1, 8.8.8.8

[domain]
name = exemple.local
```


## Sources

- [PySide6](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/index.html)