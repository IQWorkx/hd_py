# Helpdesk Visitor Management System

This is a Python Flask application for managing company visitors. It allows entry of visitor data, generates a temporary ID with a QR code, and enables login/logout using the QR code. MySQL is used as the backend database.

## Features
- Visitor data entry
- Temporary ID and QR code generation
- QR code-based login/logout

## Requirements
- Python 3.x
- MySQL server
- Flask
- mysql-connector-python
- qrcode
- pillow

## Setup
1. Create and activate a virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```sh
   pip install flask mysql-connector-python qrcode pillow
   ```
3. Configure your MySQL database connection in the app.
4. Run the application:
   ```sh
   flask run
   ```

## Notes
- Replace any placeholder credentials in the code with your actual MySQL credentials.
- The QR code image is generated for each visitor and can be scanned for login/logout.
