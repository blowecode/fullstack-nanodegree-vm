## Project Overview

The task for this project was to design a website that lists categories (genres) and items (movies) for each category. The website needed to implement CRUD and authentication functionalities. User authentication was provided by a Google API. The website is also required to provide API endpoints for information in the database.

## Requirements

The following technology was used to complete the project:

Python3
Vagrant
VirtualBox


##  How to access the project?

The following steps explain how to execute the code for this project assuming all software and data has been previously installed:

 1. Download version 3 of python.
 2. Download and install Vagrant and VirtualBox.
 3. Download the project zip file.
 4. Copy files in the zip file into the vagrant folder inside the downloaded for you virtual machine.
 5. Navigate to your virtual machine in your terminal.
 6. Cd into the vagrant folder.
 7. Launch virtual machine (`vagrant up`) and log in (`vagrant ssh`).
 8. Cd into the /vagrant folder. The python program (application.py) and other project files should already be in this folder.
 9. Run the command `python database_setup.py` to create the database.
 10. Run the command `python populate_database.py` to populate the database.
 11. Run the command `python application.py` to run the python program that starts the webpage.
 12. Open your browser and navigate to localhost:8000.
