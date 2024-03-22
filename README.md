# MongoDB with FastAPI

This is a small sample project demonstrating how to build an API with [MongoDB](https://developer.mongodb.com/) and [FastAPI](https://fastapi.tiangolo.com/).

## Get Started

To get this up and running activate your Python virtualenv (name it .venv) inside the project directory and then run the following from your terminal (edit the `MONGODB_URL` first!):
```bash
# Creating virtual environment
python -m venv .venv
# If above doesn't work try
python3 -m venv .venv

# Activate on MacOS
source .venv/bin/activate
# ...Windows
.\.venv\Scripts\activate
```

Now install the relevant dependencies.
```bash
# Install the requirements:
pip install -r requirements.txt

# Configure the location of your MongoDB database:
export MONGODB_URL="mongodb+srv://<username>:<password>@<url>/<db>?retryWrites=true&w=majority"

# Start the service:
uvicorn main:app --reload
```

Now you can load http://localhost:8000/docs in your browser

If you have any questions or suggestions, check out the [MongoDB Community Forums](https://developer.mongodb.com/community/forums/)!
