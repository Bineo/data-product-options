
# Con virtualenv 

### Windows
python -m venv venv 
.venv\Scripts\activate

### Mac/Linux
source .venv/bin/activate

### Desactivar es igual en Windows y UNIX
deactivate


# Con Conda (la 'c' en .cenv es Conda)
conda create -p .cenv

conda install --file requirements.txt

conda env remove -p .cenv

conda deactivate 