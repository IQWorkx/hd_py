import os
import uuid
import qrcode
from io import BytesIO
from datetime import datetime
from flask import Flask, request, redirect, url_for, send_file, flash, session, jsonify
import mysql.connector
import openpyxl
from theme import themed
from visitor_screens import render_visitor_form, render_qr_display, render_checkout_form
from check_screens import render_checkin_form
from admin_screens import render_admin_login_form, render_admin_dashboard, render_current_visitors, render_historical_visitors, render_admin_stats_dashboard
from ai_helpers import generate_purpose_suggestions, get_chatbot_response, analyze_visitor_patterns, predict_visitor_traffic

# Define login form
LOGIN_FORM = '''
<div class="container-fluid min-vh-100 d-flex flex-column py-4">
  <div class="row flex-grow-1 justify-content-center">
    <div class="col-md-6">
      <div class="card h-100 shadow-sm">
        <div class="card-header bg-primary text-white p-4">
          <h2 class="mb-0">Visitor Login</h2>
        </div>
        <div class="card-body p-4">
          <form method="post" action="/login">
            <div class="mb-4">
              <label class="form-label fw-medium">Enter Your Temporary ID:</label>
              <input class="form-control form-control-lg" type="text" name="temp_id" required>
            </div>
            <div class="d-grid gap-2">
              <button class="btn btn-primary btn-lg btn-raised" type="submit">
                <i class="fas fa-sign-in-alt me-2"></i>Login
              </button>
              <a class="btn btn-outline-secondary btn-lg btn-raised" href="/">
                <i class="fas fa-arrow-left me-2"></i>Back to Registration
              </a>
            </div>
          </form>
          {% with messages = get_flashed_messages() %}
            {% if messages %}
              <div class="alert alert-info mt-3">
                <ul class="mb-0">{% for msg in messages %}<li>{{ msg }}</li>{% endfor %}</ul>
              </div>
            {% endif %}
          {% endwith %}
        </div>
      </div>
    </div>
  </div>
</div>
'''

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this in production

# MySQL configuration (update with your credentials)
DB_CONFIG = {
    'user': 'ashams001',
    'password': 'iqHired@123',
    'host': '127.0.0.1',
    'database': 'hd',
    'port': 8889,
}

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.route('/')
def index():
    return render_visitor_form()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        company = request.form['company']
        purpose = request.form['purpose']
        whom_to_meet = request.form['whom_to_meet']
        temp_id = str(uuid.uuid4())[:8]
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO visitors (name, email, phone, company, purpose, whom_to_meet, temp_id, status, checkin_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
            """, (name, email, phone, company, purpose, whom_to_meet, temp_id, 'IN'))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            flash(f"Database error: {e}")
            return redirect(url_for('index'))
        return render_qr_display(name, company, temp_id)
    else:  # GET request
        temp_id = request.args.get('temp_id')
        if temp_id:
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT name, company FROM visitors WHERE temp_id=%s", (temp_id,))
                visitor = cursor.fetchone()
                cursor.close()
                conn.close()
                if visitor:
                    name, company = visitor
                    return render_qr_display(name, company, temp_id)
            except Exception as e:
                flash(f"Database error: {e}")
        return redirect(url_for('index'))

@app.route('/qr_code')
def qr_code():
    temp_id = request.args.get('temp_id')
    if not temp_id:
        return "Error: No temp_id provided", 400
    img = qrcode.make(temp_id)
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    response = send_file(buf, mimetype='image/png')
    # Add CORS headers to allow the image to be accessed by html2canvas
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET')
    return response

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template_string(themed(LOGIN_FORM))
    temp_id = request.form['temp_id']
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM visitors WHERE temp_id=%s", (temp_id,))
        row = cursor.fetchone()
        if not row:
            flash("Invalid Temp ID.")
        else:
            new_status = 'IN' if row[0] == 'OUT' else 'OUT'
            cursor.execute("UPDATE visitors SET status=%s WHERE temp_id=%s", (new_status, temp_id))
            conn.commit()
            flash(f"Status changed to {new_status}.")
        cursor.close()
        conn.close()
    except Exception as e:
        flash(f"Database error: {e}")
    return redirect(url_for('login'))

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'GET':
        return render_admin_login_form()
    username = request.form['username']
    password = request.form['password']
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session['admin_logged_in'] = True
        session['admin_username'] = username
        return redirect(url_for('admin_dashboard'))
    flash('Invalid credentials')
    return redirect(url_for('admin_login'))

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    return redirect(url_for('admin_login'))

@app.route('/migrate')
def migrate():
    schema = '''
    CREATE TABLE IF NOT EXISTS visitors (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100),
        phone VARCHAR(20),
        company VARCHAR(100) NOT NULL,
        purpose VARCHAR(255),
        whom_to_meet VARCHAR(100),
        temp_id VARCHAR(16) NOT NULL UNIQUE,
        status ENUM('IN', 'OUT') DEFAULT 'OUT',
        checkin_time DATETIME,
        checkout_time DATETIME,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    '''
    users_schema = '''
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        role ENUM('superadmin', 'admin', 'receptionist') NOT NULL DEFAULT 'receptionist',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    '''
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(schema)
        cursor.execute(users_schema)
        # Insert default superadmin if not exists
        cursor.execute("SELECT COUNT(*) FROM users WHERE username=%s", ('superadmin',))
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", ('superadmin', 'superadmin123', 'superadmin'))
        conn.commit()
        cursor.close()
        conn.close()
        return 'Migration successful: visitors and users tables created/updated, superadmin added.'
    except Exception as e:
        return f'Migration failed: {e}'

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # For dashboard stats
        cursor.execute("SELECT COUNT(*) as total FROM visitors")
        total_visitors = cursor.fetchone()['total']
        cursor.execute("SELECT COUNT(*) as today FROM visitors WHERE DATE(checkin_time) = CURDATE()")
        today_visitors = cursor.fetchone()['today']
        cursor.execute("SELECT COUNT(*) as current FROM visitors WHERE status != 'OUT'")
        current_visitors = cursor.fetchone()['current']
        cursor.execute("SELECT COUNT(*) as historical FROM visitors WHERE status = 'OUT'")
        historical_visitors = cursor.fetchone()['historical']
        # For chart: visitors per day (last 7 days)
        cursor.execute("SELECT DATE(checkin_time) as day, COUNT(*) as count FROM visitors WHERE checkin_time IS NOT NULL GROUP BY day ORDER BY day DESC LIMIT 7")
        chart_data = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        flash(f"Database error: {e}")
        total_visitors = today_visitors = current_visitors = historical_visitors = 0
        chart_data = []
    return render_admin_stats_dashboard(total_visitors, today_visitors, current_visitors, historical_visitors, chart_data)

@app.route('/admin/current-visitors')
def admin_current_visitors():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM visitors WHERE status != 'OUT' ORDER BY checkin_time DESC")
        current_visitors = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        flash(f"Database error: {e}")
        current_visitors = []
    return render_current_visitors(current_visitors)

@app.route('/admin/historical-visitors')
def admin_historical_visitors():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM visitors WHERE status = 'OUT' AND checkin_time IS NOT NULL AND checkout_time IS NOT NULL ORDER BY checkout_time DESC")
        historical_visitors = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        flash(f"Database error: {e}")
        historical_visitors = []
    return render_historical_visitors(historical_visitors)

@app.route('/admin/export')
def admin_export():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, phone, company, purpose, whom_to_meet, temp_id, status, checkin_time, checkout_time, created_at FROM visitors ORDER BY created_at DESC")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(['ID', 'Name', 'Email', 'Phone', 'Company', 'Purpose', 'Whom to Meet', 'Temp ID', 'Status', 'Check-In Time', 'Check-Out Time', 'Created At'])
        for row in rows:
            ws.append(row)
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        return send_file(output, as_attachment=True, download_name='visitors.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    except Exception as e:
        flash(f"Export failed: {e}")
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/logout_visitor/<int:visitor_id>')
def admin_logout_visitor(visitor_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE visitors SET status='OUT', checkout_time=NOW() WHERE id=%s AND status='IN'", (visitor_id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Visitor manually clocked out.')
    except Exception as e:
        flash(f"Manual clock out failed: {e}")
    return redirect(url_for('admin_dashboard'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'GET':
        return render_checkout_form()
    temp_id = request.form['temp_id']
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM visitors WHERE temp_id=%s", (temp_id,))
        row = cursor.fetchone()
        if not row:
            flash("Invalid Temp ID.")
        elif row[0] == 'OUT':
            flash("Visitor already checked out.")
        else:
            cursor.execute("UPDATE visitors SET status='OUT' WHERE temp_id=%s", (temp_id,))
            conn.commit()
            flash("Checkout successful.")
        cursor.close()
        conn.close()
    except Exception as e:
        flash(f"Database error: {e}")
    return redirect(url_for('checkout'))

@app.route('/checkin', methods=['GET', 'POST'])
def checkin():
    if request.method == 'GET':
        return render_checkin_form()
    temp_id = request.form['temp_id']
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM visitors WHERE temp_id=%s", (temp_id,))
        row = cursor.fetchone()
        if not row:
            flash("Invalid Temp ID.")
        elif row[0] == 'IN':
            flash("Visitor already checked in.")
        else:
            cursor.execute("UPDATE visitors SET status='IN', checkin_time=NOW(), checkout_time=NULL WHERE temp_id=%s", (temp_id,))
            conn.commit()
            flash("Check-in successful.")
        cursor.close()
        conn.close()
    except Exception as e:
        flash(f"Database error: {e}")
    return redirect(url_for('checkin'))

# Register a Jinja2 filter for datetime formatting
@app.template_filter('datetime')
def format_datetime(value, format='medium'):
    if not value:
        return ''
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value)
        except Exception:
            return value
    if format == 'full':
        fmt = "%A, %d %B %Y, %I:%M %p"
    elif format == 'medium':
        fmt = "%d %b %Y, %I:%M %p"
    else:
        fmt = "%Y-%m-%d %H:%M"
    return value.strftime(fmt)

# AI API Endpoints
@app.route('/api/purpose-suggestions')
def api_purpose_suggestions():
    company = request.args.get('company', '')
    if not company:
        return jsonify({'error': 'Company name is required', 'suggestions': []})

    suggestions = generate_purpose_suggestions(company)
    return jsonify({'suggestions': suggestions})

@app.route('/api/chatbot', methods=['POST'])
def api_chatbot():
    data = request.json
    if not data or 'message' not in data:
        return jsonify({'error': 'Message is required', 'response': 'Please provide a message'})

    message = data['message']
    visitor_name = data.get('visitor_name', '')

    response = get_chatbot_response(message, visitor_name)
    return jsonify({'response': response})

@app.route('/api/visitor-analytics')
def api_visitor_analytics():
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized access'})

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM visitors WHERE checkin_time IS NOT NULL")
        visitors_data = cursor.fetchall()
        cursor.close()
        conn.close()

        analytics = analyze_visitor_patterns(visitors_data)
        return jsonify(analytics)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/visitor-predictions')
def api_visitor_predictions():
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized access'})

    days = request.args.get('days', 7, type=int)

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM visitors WHERE checkin_time IS NOT NULL")
        visitors_data = cursor.fetchall()
        cursor.close()
        conn.close()

        predictions = predict_visitor_traffic(visitors_data, days)
        return jsonify(predictions)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True,  port=6100)
