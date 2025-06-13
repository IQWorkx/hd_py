from flask import render_template_string, url_for

LIGHT_THEME_CSS = '''
<style>
body { background: #f8f9fa; color: #222; font-family: Arial, sans-serif; }
h2 { color: #007bff; }
form { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px #eee; max-width: 400px; margin: 20px auto; }
input[type=text], input[type=email], input[type=password] {
  width: 100%; padding: 8px; margin: 8px 0 16px 0; border: 1px solid #ccc; border-radius: 4px;
}
input[type=submit] {
  background: #007bff; color: #fff; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer;
}
input[type=submit]:hover { background: #0056b3; }
table { width: 100%; border-collapse: collapse; margin: 20px 0; background: #fff; }
th, td { border: 1px solid #dee2e6; padding: 8px; text-align: left; }
th { background: #e9ecef; }
a { color: #007bff; text-decoration: none; }
a:hover { text-decoration: underline; }
ul { color: #d9534f; }
</style>
'''

def themed(html):
    return LIGHT_THEME_CSS + html

# Visitor Entry Form
VISITOR_FORM = '''
<h2>Visitor Entry</h2>
<form method="post" action="/register">
  Name: <input type="text" name="name" required><br>
  Email: <input type="email" name="email" required><br>
  Phone: <input type="text" name="phone" required><br>
  Company: <input type="text" name="company" required><br>
  Purpose of Visit: <input type="text" name="purpose" required><br>
  Whom to Meet: <input type="text" name="whom_to_meet" required><br>
  <input type="submit" value="Register">
</form>
{% with messages = get_flashed_messages() %}
  {% if messages %}
    <ul>{% for msg in messages %}<li>{{ msg }}</li>{% endfor %}</ul>
  {% endif %}
{% endwith %}
'''

def render_visitor_form():
    return render_template_string(themed(VISITOR_FORM))

# QR Display
QR_DISPLAY = '''
<h2>Visitor Registered</h2>
<p>Name: {{ name }}</p>
<p>Company: {{ company }}</p>
<p>Temp ID: {{ temp_id }}</p>
<img src="{{ url_for('qr_code', temp_id=temp_id) }}" alt="QR Code"><br>
<p>Scan this QR code at the <a href="/checkin">Check-In</a> counter to check in.</p>
<a href="/">Back to Entry</a>
'''

def render_qr_display(name, company, temp_id):
    return render_template_string(themed(QR_DISPLAY), name=name, company=company, temp_id=temp_id)

# Check-In Form
CHECKIN_FORM = '''
<h2>Visitor Check-In</h2>
<form method="post" action="/checkin">
  Scan QR Code or Enter Temp ID: <input type="text" name="temp_id" required><br>
  <input type="submit" value="Check In">
</form>
{% with messages = get_flashed_messages() %}
  {% if messages %}
    <ul>{% for msg in messages %}<li>{{ msg }}</li>{% endfor %}</ul>
  {% endif %}
{% endwith %}
'''

def render_checkin_form():
    return render_template_string(themed(CHECKIN_FORM))

# Checkout Form
CHECKOUT_FORM = '''
<h2>Visitor Checkout</h2>
<form method="post" action="/checkout">
  Scan QR Code or Enter Temp ID: <input type="text" name="temp_id" required><br>
  <input type="submit" value="Checkout">
</form>
{% with messages = get_flashed_messages() %}
  {% if messages %}
    <ul>{% for msg in messages %}<li>{{ msg }}</li>{% endfor %}</ul>
  {% endif %}
{% endwith %}
'''

def render_checkout_form():
    return render_template_string(themed(CHECKOUT_FORM))

# Admin Login Form
ADMIN_LOGIN_FORM = '''
<h2>Admin Login</h2>
<form method="post" action="/admin/login">
  Username: <input type="text" name="username" required><br>
  Password: <input type="password" name="password" required><br>
  <input type="submit" value="Login">
</form>
{% with messages = get_flashed_messages() %}
  {% if messages %}
    <ul>{% for msg in messages %}<li>{{ msg }}</li>{% endfor %}</ul>
  {% endif %}
{% endwith %}
'''

def render_admin_login_form():
    return render_template_string(themed(ADMIN_LOGIN_FORM))

# Admin Dashboard
def render_admin_dashboard(visitors):
    dashboard_html = '''
    <h2>Admin Dashboard</h2>
    <a href="/admin/export">Export to Excel</a> |
    <a href="/admin/logout">Logout</a>
    <table border="1">
      <tr><th>ID</th><th>Name</th><th>Email</th><th>Phone</th><th>Company</th><th>Purpose</th><th>Whom to Meet</th><th>Temp ID</th><th>Status</th><th>Created At</th><th>Actions</th></tr>
      {% for v in visitors %}
        <tr>
          <td>{{ v.id }}</td><td>{{ v.name }}</td><td>{{ v.email }}</td><td>{{ v.phone }}</td><td>{{ v.company }}</td><td>{{ v.purpose }}</td><td>{{ v.whom_to_meet }}</td><td>{{ v.temp_id }}</td><td>{{ v.status }}</td><td>{{ v.created_at }}</td>
          <td>{% if v.status == 'IN' %}<a href="/admin/logout_visitor/{{ v.id }}">Manual Logout</a>{% endif %}</td>
        </tr>
      {% endfor %}
    </table>
    '''
    return render_template_string(themed(dashboard_html), visitors=visitors)
