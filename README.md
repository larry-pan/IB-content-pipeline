Welcome to the AI IB Question Generator!

The easiest (and coolest) way to run the application is just run demo.exe
This will launch the backend server with the frontend interface automatically served at:
http://localhost:8000

Note: The exe uses my cohere free api key, which is limited to 10 api requests per minute.
Generating 1 question uses ~6 requests, so it may break if you spam it.


Running examples.py
-------------------
There is a file named examples.py inside the backend/ directory that contains example scripts.

Cohere API Key Required:
To use examples.py, you must:

1. Obtain a Cohere API key from https://cohere.com
2. Create a `.env` file inside the backend/ folder with:

    COHERE_API_KEY=your_api_key_here

Make sure your virtual environment is activated and all required dependencies are installed.
You can pip install -r requirements.txt in the backend folder.
