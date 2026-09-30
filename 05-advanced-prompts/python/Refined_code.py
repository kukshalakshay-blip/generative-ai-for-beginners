import os

import re

from flask import Flask, request, Response



# Load configuration from environment variable

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(32)  # Random secure key for potential future use



# Define a safe pattern: alphanumeric, spaces, hyphens, and periods

NAME_PATTERN = re.compile(r'^[a-zA-Z0-9 .\-]{1,50}$')



def sanitize_name(raw_name: str) -> str:

    """

    Validates and sanitizes the 'name' input.

    Rejects inputs that are empty, too long, or contain disallowed characters.

    """

    if not raw_name or not isinstance(raw_name, str):

        raise ValueError("Name cannot be empty")

    

    # Strip leading/trailing whitespace

    name = raw_name.strip()

    

    # Check against allowed pattern (letters, digits, space, hyphen, dot)

    if not NAME_PATTERN.match(name):

        raise ValueError("Name contains invalid characters")

    

    return name



@app.route('/health', methods=['GET'])

def health_check():

    """Simple health check endpoint for production monitoring."""

    return Response('OK', status=200, mimetype='text/plain')



@app.route('/', methods=['GET'])

def hello():

    raw_name = request.args.get('name', 'World')

    

    try:

        safe_name = sanitize_name(raw_name)

    except ValueError as e:

        # Return a 400 Bad Request with a generic message (don't leak details)

        return Response('Invalid name provided', status=400, mimetype='text/plain')

    

    # Explicitly specify text/plain to avoid browser HTML interpretation

    return Response(f'Hello, {safe_name}!', status=200, mimetype='text/plain')



# For local development only - in production, run with:

# gunicorn -w 4 -b 0.0.0.0:8000 'app:app'

if __name__ == '__main__':

    app.run(debug=False, host='0.0.0.0', port=5000)

