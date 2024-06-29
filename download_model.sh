#!/bin/bash
FILE_ID="1wcpNzvvJjTIcoBzz9ZOGXrnqlP2BRWhA"  # Replace with your actual file ID
FILE_NAME="model.pkl"

curl -L -o ${FILE_NAME} "https://drive.google.com/uc?export=download&id=${FILE_ID}"
