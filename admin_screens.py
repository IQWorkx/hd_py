from flask import render_template_string
from theme import themed

def render_admin_login_form():
    ADMIN_LOGIN_FORM = '''
    <div class="container mt-5">
    <div class="row justify-content-center">
    <div class="col-md-6">
    <div class="card p-4">
    <h2 class="mb-4">Admin Login</h2>
    <form method="post" action="/admin/login">
      <div class="mb-3">
        <label>Username:</label>
        <input class="form-control" type="text" name="username" required>
      </div>
      <div class="mb-3">
        <label>Password:</label>
        <input class="form-control" type="password" name="password" required>
      </div>
      <input class="btn btn-primary" type="submit" value="Login">
    </form>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul>{% for msg in messages %}<li>{{ msg }}</li>{% endfor %}</ul>
      {% endif %}
    {% endwith %}
    </div></div></div></div>
    '''
    return render_template_string(themed(ADMIN_LOGIN_FORM, admin=True))

def render_admin_dashboard(current_visitors, historical_visitors):
    dashboard_html = '''
    <div class="container mt-4">
    <h2>Current Visitors</h2>
    <table class="table table-bordered table-striped">
      <thead class="table-light">
      <tr><th>ID</th><th>Name</th><th>Email</th><th>Phone</th><th>Company</th><th>Purpose</th><th>Whom to Meet</th><th>Temp ID</th><th>Status</th><th>Check-In</th><th>Duration (min)</th><th>Actions</th></tr>
      </thead>
      <tbody>
      {% for v in current_visitors %}
        <tr>
          <td>{{ v.id }}</td><td>{{ v.name }}</td><td>{{ v.email }}</td><td>{{ v.phone }}</td><td>{{ v.company }}</td><td>{{ v.purpose }}</td><td>{{ v.whom_to_meet }}</td><td>{{ v.temp_id }}</td><td>{{ v.status }}</td><td>{{ v.checkin_time }}</td><td>{{ v.duration or 0 }}</td>
          <td><a class="btn btn-sm btn-warning" href="/admin/logout_visitor/{{ v.id }}">Clock Out</a></td>
        </tr>
      {% endfor %}
      </tbody>
    </table>
    <h2 class="mt-5">Visitor History</h2>
    <table class="table table-bordered table-striped">
      <thead class="table-light">
      <tr><th>ID</th><th>Name</th><th>Email</th><th>Phone</th><th>Company</th><th>Purpose</th><th>Whom to Meet</th><th>Temp ID</th><th>Status</th><th>Check-In</th><th>Check-Out</th><th>Duration (min)</th></tr>
      </thead>
      <tbody>
      {% for v in historical_visitors %}
        <tr>
          <td>{{ v.id }}</td><td>{{ v.name }}</td><td>{{ v.email }}</td><td>{{ v.phone }}</td><td>{{ v.company }}</td><td>{{ v.purpose }}</td><td>{{ v.whom_to_meet }}</td><td>{{ v.temp_id }}</td><td>{{ v.status }}</td><td>{{ v.checkin_time }}</td><td>{{ v.checkout_time }}</td><td>{{ v.duration or 0 }}</td>
        </tr>
      {% endfor %}
      </tbody>
    </table>
    </div>
    '''
    return render_template_string(themed(dashboard_html, admin=True), current_visitors=current_visitors, historical_visitors=historical_visitors)
