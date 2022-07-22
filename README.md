# WAF Tools
Repository containing all my WAF tools.

## Authors/Maintainers
- Bernardo Fichera (bernardo.fichera@epfl.ch)

## Available Tools
- Arpack (https://www.caam.rice.edu/software/ARPACK/)
- Assimp (https://github.com/assimp/assimp)
- ...

## ToDo
Here is a list of improvements:
- Adding CUDA support for eigen
- Adding PGI compiler
- boost, corrade, magnum tools need to be completed
- Generate cmake files

## Install the package
In order to install the package in `.local` run
```sh
pip(pip3) install .
```
For local installation in the current directory
```sh
pip(pip3) install -e .
```
Let sudo see binaries in the your local path. Add this alias to your `.bashrc`(`.zshrc`)
```
alias sudo="sudo -E env 'PATH=$PATH'"
```