# DVF Data visualization python project

Just a little dataviz projet with plotly, django, pygal and pandas.
Quick start:
```
git clone https://github.com/Joytide/dvf-dataviz.git
cd dvf-dataviz
pip3 install -r requirements.txt
wget https://www.data.gouv.fr/fr/datasets/r/3004168d-bec4-44d9-a781-ef16f41856a2 -O ./dataviz/script/valeursfoncieres-2019.txt
wget https://www.data.gouv.fr/fr/datasets/r/90a98de0-f562-4328-aa16-fe0dd1dca60f -O ./dataviz/script/valeursfoncieres-2020.txt
python3 manage.py migrate
python manage.py runserver
```
