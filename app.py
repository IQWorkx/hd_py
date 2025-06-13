import os
import uuid
import qrcode
from io import BytesIO
from flask import Flask, request, redirect, url_for, send_file, flash, session
import mysql.connector
import openpyxl
from visitor_screens import render_visitor_form, render_qr_display
from check_screens import render_checkin_form, render_checkout_form
from admin_screens import render_admin_login_form, render_admin_dashboard

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

@app.route('/register', methods=['POST'])
def register():
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

@app.route('/qr/<temp_id>')
def qr_code(temp_id):
    img = qrcode.make(temp_id)
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

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
        return redirect(url_for('admin_dashboard'))
    flash('Invalid credentials')
    return redirect(url_for('admin_login'))

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
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
        cursor.execute("SELECT *, TIMESTAMPDIFF(MINUTE, checkin_time, NOW()) as duration FROM visitors WHERE status!='OUT' ORDER BY checkin_time DESC")
        current_visitors = cursor.fetchall()
        cursor.execute("SELECT *, TIMESTAMPDIFF(MINUTE, checkin_time, checkout_time) as duration FROM visitors WHERE status='OUT' AND checkin_time IS NOT NULL AND checkout_time IS NOT NULL ORDER BY checkout_time DESC")
        historical_visitors = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        flash(f"Database error: {e}")
        current_visitors = []
        historical_visitors = []
    return render_admin_dashboard(current_visitors, historical_visitors)

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

if __name__ == '__main__':
    app.run(debug=True,  port=6100)
