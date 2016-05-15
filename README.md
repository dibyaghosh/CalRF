# Cal Room Finder

Uses the Schedule of Classes from UC Berkeley to find open rooms throught campus to study.
This app requires a class schedule pared, which is included in the repository.

This site is running live at http://dibya.xyz/roomfinder/

# Installation

(Optional) Create and enter a conda environment using

	conda create --name ENV_NAME python=3.4

Install from the list of requirements.

	pip install -r requirements.txt

# How to Run


2) To run the visualization, run the server and load the webpage: localhost:5000

	python -i server.py



# Screenshots

![Dashboard](/screenshots/dashboard.png?raw=true "Dashboard of Buildings")

![Building View](/screenshots/building.png?raw=true "Building Views")


# Development

The project structure is as following

- CourseWhere.csv - Models for SQLAlchemy ORM
- index.html  - The self-contained single-page application 
- server.py - The main Flask Application
- static/ 	- All HTML/CSS/JS files (None at the moment)

