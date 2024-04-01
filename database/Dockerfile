# Use the official MySQL image as base
FROM mysql:8.1.0

# Copy the SQL script to create the table into the container
COPY init.sql /docker-entrypoint-initdb.d/

# Expose MySQL port
EXPOSE 3306