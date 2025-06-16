# AI-Powered Visitor Management System

This is a Python Flask application for managing company visitors with integrated AI capabilities. It allows entry of visitor data, generates a temporary ID with a QR code, enables login/logout using the QR code, and provides AI-powered features like smart recommendations, chatbot assistance, and visitor analytics. MySQL is used as the backend database.

## Features
- Visitor data entry with AI-powered purpose suggestions
- Temporary ID and QR code generation
- QR code-based login/logout
- QR code sharing via WhatsApp and Bluetooth
- AI chatbot for visitor assistance
- AI-powered visitor analytics and insights
- Predictive visitor traffic forecasting

## Requirements
- Python 3.x
- MySQL server
- Flask
- mysql-connector-python
- qrcode
- pillow
- openai (for AI chatbot)
- scikit-learn (for machine learning)
- pandas (for data analysis)
- numpy (for numerical operations)
- matplotlib (for visualization)

## Setup
1. Create and activate a virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Configure your MySQL database connection in the app.
4. The application uses port 6100 by default (configured in .flaskenv). Run the application:
   ```sh
   flask run
   ```

   If port 6100 is already in use, you can modify the port in the .flaskenv file or specify a different port:
   ```sh
   flask run --port=7000
   ```

## Notes
- Replace any placeholder credentials in the code with your actual MySQL credentials.
- The QR code image is generated for each visitor and can be scanned for login/logout.
- To enable the OpenAI-powered chatbot, uncomment the `openai.api_key` line in `ai_helpers.py` and add your API key.
- The AI features use a combination of rule-based approaches and machine learning techniques. In a production environment, you may want to fine-tune these models with your specific data.
- The visitor analytics and predictions become more accurate as more visitor data is collected.

## Internationalization (i18n)
This application supports multiple languages: English, Hindi, Kannada, and Arabic. All user-facing text is translatable.

### Updating Translations
1. After editing any `.po` translation files in `translations/<lang>/LC_MESSAGES/messages.po`, compile them to `.mo` files:
   ```sh
   pybabel compile -d translations
   ```
   This makes your translations available to the app.

2. To extract new/changed strings and update all translation files:
   ```sh
   pybabel extract -F babel.cfg -o translations/messages.pot .
   pybabel update -i translations/messages.pot -d translations -l en -l hi -l kn -l ar
   ```

3. Edit the `.po` files for each language and repeat the compile step above.

### Language Switcher
- A language switcher is available in both the admin and visitor headers. Users can select their preferred language from the dropdown.
