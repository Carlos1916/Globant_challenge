# Use the official Python image as the base image
FROM python:3.9

# install postgresql-client
RUN apt-get update && apt-get install -y postgresql-client

# Set environment variable for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /magneton

# Copy the requirements file to the container
COPY requirements.txt /magneton/requirements.txt

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the application code to the container
COPY . /magneton/

# Expose the port on which your Django app will run (change it if needed)
EXPOSE 8000

# Expose the port on which your Postgres database will run (change it if needed)
EXPOSE 5433


# Collect static files
RUN python manage.py collectstatic --noinput

# Install Nginx
RUN apt-get update && apt-get install -y nginx

# Copy Nginx configuration file to the container
COPY nginx.conf /etc/nginx/sites-available/default

# Start Nginx
CMD service nginx start && gunicorn --bind 0.0.0.0:8000 --preload magneton.wsgi:application




