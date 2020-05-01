# image-gen
This project generates a labeled data set using a set of 3D models.

# How to Run
`blender --background base.blend --python generate_image.py`

# Setup 
## Install Requirements
`pip install -r requirements.txt`

## Create and Activate Virtual Environment (Optional)
Install the virtual environment package

`pip install virtualenv`

Create a new virtual environment (You may choose your own name, but here we used "venv")

`virtualenv venv`

Activate the Virtual Environment

`venv\Scripts\activate`

Or on mac:
`source venv/bin/activate`