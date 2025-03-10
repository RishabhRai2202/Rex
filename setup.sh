#!/bin/bash

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null
then
    echo "Python 3 not found! Please install Python 3 and try again."
    exit 1
fi

# Create Virtual Environment
python3 -m venv myenv

# Activate Virtual Environment
source myenv/bin/activate

# Install Dependencies
pip install --upgrade pip
pip install -r requirements.txt

echo "Setup complete! Run './start.sh' to execute the project."