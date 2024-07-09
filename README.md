# FastAPI OBD-II Reader

This project utilizes FastAPI to create a web API for retrieving car information via OBD-II (On-Board Diagnostics) adapter.

## Setup Instructions

### Clone the Repository

```bash
## clone the repository
git clone https://github.com/ckaraze/obdreader_project.git
cd obdreader_project

## Create and activate a virtual environment:
python -m venv obdenv
source obdenv/bin/activate  # On Windows use `obdenv\Scripts\activate`

## Install dependencies:
pip install -r requirements.txt

# install FastAPI
# pip install fastapi

# upgrade pip:
# pip install --upgrade pip

# install uvicorn
# pip install uvicorn

# install pyobd library
# pip install pyobd

# install obd library
# pip install obd

# install \ upgrade pint
# pip install --upgrant pint

## Run FastAPI
uvicorn main:app --reload

stop running
crtl + c