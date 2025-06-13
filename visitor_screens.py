from flask import render_template_string, url_for
from theme import themed

VISITOR_FORM = '''
<div class="container mt-5">
  <div class="row justify-content-center">
    <div class="col-md-6">
      <div class="card p-4">
        <h2 class="mb-4">Visitor Entry</h2>
        <form method="post" action="/register">
          <div class="mb-3">
            <label>Name:</label>
            <input class="form-control" type="text" name="name" required>
          </div>
          <div class="mb-3">
            <label>Email:</label>
            <input class="form-control" type="email" name="email" required>
          </div>
          <div class="mb-3">
            <label>Phone:</label>
            <input class="form-control" type="text" name="phone" required>
          </div>
          <div class="mb-3">
            <label>Company:</label>
            <input class="form-control" type="text" name="company" required>
          </div>
          <div class="mb-3">
            <label>Purpose of Visit:</label>
            <input class="form-control" type="text" name="purpose" required>
          </div>
          <div class="mb-3">
            <label>Whom to Meet:</label>
            <input class="form-control" type="text" name="whom_to_meet" required>
          </div>
          <input class="btn btn-primary" type="submit" value="Register">
        </form>
        <a class="btn btn-danger mt-3 w-100" href="/checkout">Check Out</a>
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

def render_visitor_form():
    return render_template_string(themed(VISITOR_FORM))

QR_DISPLAY = '''
<div class="container mt-5">
  <div class="row justify-content-center">
    <div class="col-md-6">
      <div class="card p-4 text-center">
        <h2 class="mb-4">Visitor Registered</h2>
        <p>Name: {{ name }}</p>
        <p>Company: {{ company }}</p>
        <p>Temp ID: {{ temp_id }}</p>
        <img src="{{ url_for('qr_code', temp_id=temp_id) }}" alt="QR Code" class="mb-3"><br>
        <p>Scan this QR code at the <a href="/checkin">Check-In</a> counter to check in.</p>
        <a class="btn btn-link" href="/">Back to Entry</a>
        <a class="btn btn-danger mt-3" href="/checkout">Check Out</a>
      </div>
    </div>
  </div>
</div>
'''

def render_qr_display(name, company, temp_id):
    return render_template_string(themed(QR_DISPLAY), name=name, company=company, temp_id=temp_id)

CHECKOUT_FORM = '''
<div class="container mt-5">
  <div class="row justify-content-center">
    <div class="col-md-6">
      <div class="card p-4">
        <h2 class="mb-4">Visitor Checkout</h2>
        <form method="post" action="/checkout">
          <div class="mb-3">
            <label>Scan QR Code or Enter Temp ID:</label>
            <input class="form-control" type="text" name="temp_id" id="temp_id" required>
          </div>
          <input class="btn btn-danger" type="submit" value="Checkout">
        </form>
        <button class="btn btn-secondary mt-3" onclick="startScan()">Scan QR Code</button>
        <div id="qr-reader" style="width:100%"></div>
        {% with messages = get_flashed_messages() %}
          {% if messages %}
            <ul>{% for msg in messages %}<li>{{ msg }}</li>{% endfor %}</ul>
          {% endif %}
        {% endwith %}
      </div>
    </div>
  </div>
</div>
<script src="https://unpkg.com/html5-qrcode" type="text/javascript"></script>
<script>
function startScan() {
  document.getElementById('qr-reader').innerHTML = '';
  var qr = new Html5Qrcode("qr-reader");
  qr.start({ facingMode: "environment" }, { fps: 10, qrbox: 250 },
    qrCodeMessage => {
      document.getElementById('temp_id').value = qrCodeMessage;
      qr.stop();
    },
    errorMessage => {})
    .catch(err => {});
}
</script>
'''

def render_checkout_form():
    return render_template_string(themed(CHECKOUT_FORM))
