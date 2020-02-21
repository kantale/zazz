# zazz

# Installation with conda
This guide assumes that you have [conda](https://docs.conda.io/en/latest/) installed.

Create a conda virtual python environment:
```bash
conda create -n python_zazz python=3.7
```

Activate it:
```bash
source activate python_zazz
```

Install python packages:
```bash
pip install django==2.1.5 pandas simplejson xlrd 
```

Create initial model file:
```bash
cp zazz/models_init.py zazz/models.py 
```

Build the database
```bash
python manage.py makemigrations zazz
python manage.py migrate
```

Insert dummy/test data in the database (Optional):
```bash
python zazz.py 
```

Run with:
```bash
python manage.py runserver 0.0.0.0:8300
```

# Contact
* [Alexandros Kanterakis](mailto:kantale@ics.forth.gr)
* [Lena Latsoudis](mailto:latsoudi@ics.forth.gr) 

