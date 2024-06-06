# Installation

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

:::{seealso}
*venv* https://docs.python.org/3/library/venv.html
:::

## Install the package

Install the package from the corresponding wheel using `pip`

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

```

TBC

