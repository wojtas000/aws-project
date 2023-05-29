# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local directory to the container
COPY . .

# Expose the default Streamlit port
EXPOSE 8501

# Set the command to run the Streamlit app when the container starts
CMD ["streamlit", "run", "user_interface/authentication.py"]

# docker build -t streamlit-app .
# docker run -p 8501:8501 streamlit-app 
