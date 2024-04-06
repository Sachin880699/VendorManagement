

# Vendor Management System
___________________________________________________________

# setup

The first thing to do is to clone this repository

        git clone https://github.com/Sachin880699/VendorManagement
        cd VendorManagement

create a virtual environment to install dependencies in and active it

        python3 -m venv env
        source env/bin/activate

Then install the dependencies:

        pip install -r requirements.txt


Note the (env) in front of the prompt. This indicates that this terminal session operates in a virtual environment set up by virtualenv2

Once pip has finished downloading the dependencies:


        (env)$ cd project
        (env)$ python manage.py runserver

