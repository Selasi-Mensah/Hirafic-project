#!/usr/bin/env python3
""" Include the insertion for dumpy data"""
from models.user import db, User
from models.client import Client
from models.artisan import Artisan
from models.booking import Booking
from __init__ import create_app
from datetime import datetime
import csv


def insert_data_from_csv_file(file_path, model, field_map):
    """
    Generic function to insert data from a CSV file into the specified model.
    :param file_path: Path to the CSV file.
    :param model:
        The model class (e.g., User, Client, Artisan, Booking).
    :param field_map:
        A dictionary mapping column indices from CSV to model fields.
    """
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Skip the header row

        # Create the Flask app
        app = create_app()

        # Ensure the app context is active when interacting with the database
        with app.app_context():
            try:
                for row in reader:
                    # Create a dictionary of field names and values
                    data = {
                        field: row[index]
                        for field, index in field_map.items()
                    }

                    # Handle date fields
                    if 'request_date' in data:
                        try:
                            # Convert request_date to datetime format
                            data['request_date'] = datetime.strptime(
                                data['request_date'], '%Y-%m-%d %H:%M:%S')
                        except ValueError:
                            print(f"Error: {data['request_date']}")
                            continue

                    if 'completion_date' in data:
                        try:
                            # Convert completion_date to datetime format
                            data['completion_date'] = datetime.strptime(
                                data['completion_date'], '%Y-%m-%d %H:%M:%S')
                        except ValueError:
                            print(f"Error: {data['completion_date']}")
                            continue

                    # Create model instance using unpacked data dictionary
                    instance = model(**data)

                    # Add to session
                    db.session.add(instance)

                db.session.commit()
                print(f"Data inserted successfully, {model.__name__} table.")
            except Exception as e:
                db.session.rollback()  # Rollback in case of error
                print(f"Error occurred, {model.__name__} table: {e}")


def insert_data():
    # Define field mappings for each table
    # (indexing corresponds to columns in the CSV)

    # For User table (id,username,email,phone_number,role,location,password)
    user_field_map = {
        'id': 0,
        'username': 1,
        'email': 2,
        'phone_number': 3,
        'role': 4,
        'location': 5,
        'password': 6
    }
    insert_data_from_csv_file(
        './dataset/users_table.csv', User, user_field_map)

    # For Client table (id,user_id,name,email,password,location,phone_number)
    client_field_map = {
        'id': 0,
        'user_id': 1,
        'name': 2,
        'email': 3,
        'password': 4,
        'location': 5,
        'phone_number': 6
    }
    insert_data_from_csv_file(
        './dataset/clients_table.csv', Client, client_field_map)

    # For Artisan table (id,user_id,name,email,password,location,phone_number
    # ,specialization,skills,salary_per_hour)
    artisan_field_map = {
        'id': 0,
        'user_id': 1,
        'name': 2,
        'email': 3,
        'password': 4,
        'location': 5,
        'phone_number': 6,
        'specialization': 7,
        'skills': 8,
        'salary_per_hour': 9
    }
    insert_data_from_csv_file(
        './dataset/artisans_table.csv', Artisan, artisan_field_map)

    # For Booking table (title,status,request_date,completion_date,
    # details,client_id,artisan_id)
    booking_field_map = {
        'title': 0,
        'status': 1,
        'request_date': 2,
        'completion_date': 3,
        'details': 4,
        'client_id': 5,
        'artisan_id': 6
    }
    insert_data_from_csv_file(
        './dataset/bookings_table.csv', Booking, booking_field_map)


if __name__ == '__main__':
    # Call the function to insert data for all tables
    insert_data()
