# Installation

It is assumed that [Python 3.8 or above](https://www.python.org/) has been installed
on the system.

## Create a virtual environment

Before proceeding with installation, 
it is recommended to create a virtual environment
where to install this and other packages:

```shell
python -m venv .venv
```

Then activate it. In Windows Powershell:
```powershell
PS C:\> .venv/bin/Activate.ps1
```
On Linux and MacOS
```bash
$ source .venv/bin/activate
```

:::{}
*venv* https://docs.python.org/3/library/venv.html
:::

## Install the package

Install the package from the corresponding wheel using `pip`

{manual-installation}
:::{error}
The following command works only if the repository is public.
Since it isn't the case, it is recommended to manually
download the wheel from
https://github.com/LucaLeonx/MAPF_pii_Project/blob/main/dist/mapfbench-1.0-py3-none-any.whl
and install with:
```shell
pip install -U /path/to/downloaded/file
```
:::

```shell
 pip install -U mapfbench @ git+https://github.com/LucaLeonx/MAPF_pii_Project#subdirectory=dist
```
Check that the command line tools are correctly installing by running:
```shell
 mapfbench --help
```
to show the default help message

## Build from source

Clone the project repository

```shell
 git clone https://github.com/LucaLeonx/MAPF_pii_Project.git
```

Install dependencies, including optional ones
```shell
 cd Mapf_pii_Project
 pip install -U .[build, test, docs]
```

This project is packaged using [setuptools](https://pypi.org/project/setuptools/)
To generate the packages, from outside the project directory
```shell
python -m build ./MAPF_pii_Project
```

Now the packaged wheel is available under MAPF_pii_Project/dist and can be
manually installed

```shell
pip install -U ./MAPF_pii_Project/dist/mapfbench-1.0-py3-none-any.whl
```

To build the HTML version of the documentation using [Sphinx](https://www.sphinx-doc.org/en/master/index.html) run
```shell
sphinx-build -M html ./MAPF_pii_Project/docs ./MAPF_pii_Project/docs/_build
```

The documentation will be available under ./MAPF_pii_Project/docs/_build
and is written using [MyST Markdown dialect](https://myst-parser.readthedocs.io/en/latest/)




