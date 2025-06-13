from flask import render_template_string
from theme import themed

CHECKIN_FORM = '''
<div class="container mt-5">
  <div class="row justify-content-center">
    <div class="col-md-6">
      <div class="card p-4">
        <h2 class="mb-4">Visitor Check-In</h2>
        <form method="post" action="/checkin">
          <div class="mb-3">
            <label>Scan QR Code or Enter Temp ID:</label>
            <input class="form-control" type="text" name="temp_id" required>
          </div>
          <input class="btn btn-success" type="submit" value="Check In">
        </form>
        {% with messages = get_flashed_messages() %}
          {% if messages %}
            <ul>{% for msg in messages %}<li>{{ msg }}</li>{% endfor %}</ul>
          {% endif %}
        {% endwith %}
      </div>
    </div>
  </div>
</div>
'''

def render_checkin_form():
    return render_template_string(themed(CHECKIN_FORM))

CHECKOUT_FORM = '''
<div class="container mt-5">
  <div class="row justify-content-center">
    <div class="col-md-6">
      <div class="card p-4">
        <h2 class="mb-4">Visitor Checkout</h2>
        <form method="post" action="/checkout">
          <div class="mb-3">
            <label>Scan QR Code or Enter Temp ID:</label>
            <input class="form-control" type="text" name="temp_id" required>
          </div>
          <input class="btn btn-danger" type="submit" value="Checkout">
        </form>
        {% with messages = get_flashed_messages() %}
          {% if messages %}
            <ul>{% for msg in messages %}<li>{{ msg }}</li>{% endfor %}</ul>
          {% endif %}
        {% endwith %}
      </div>
    </div>
  </div>
</div>
'''

def render_checkout_form():
    return render_template_string(themed(CHECKOUT_FORM))
