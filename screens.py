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
  background: #007bff; color: #fff; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer,
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
{% include 'visitor_header.html' %}
<div class="container py-4" style="min-height: 100vh;">
  <div class="row justify-content-center align-items-start g-4">
    <!-- Checkout form -->
    <div class="col-12 col-lg-7 d-flex align-items-stretch">
      <div class="card w-100 shadow-sm d-flex flex-column justify-content-start">
        <div class="card-header bg-primary text-white p-3">
          <h3 class="mb-0">Visitor Checkout</h3>
        </div>
        <div class="card-body p-4">
          <form method="post" action="/checkout">
            <div class="mb-3">
              <label class="form-label fw-medium">Scan QR Code or Enter Temp ID:</label>
              <div class="input-group mb-2">
                <input class="form-control form-control-lg" type="text" name="temp_id" id="tempIdInput" required placeholder="Temp ID or scan QR...">
              </div>
              <div class="d-grid mb-2">
                <button type="button" class="btn btn-success btn-lg custom-green-btn" id="startScanBtn">
                  <i class="fas fa-qrcode"></i> Scan QR
                </button>
              </div>
              <div id="qr-reader" style="width:100%;display:none;"></div>
            </div>
            <button type="submit" class="btn btn-danger btn-lg w-100 custom-red-btn">Checkout</button>
          </form>
          {% with messages = get_flashed_messages() %}
            {% if messages %}
              <ul class="mt-3">
                {% for msg in messages %}
                  <li class="text-danger">{{ msg }}</li>
                {% endfor %}
              </ul>
            {% endif %}
          {% endwith %}
        </div>
      </div>
    </div>
    <!-- AI Agent -->
    <div class="col-12 col-lg-5 d-flex align-items-stretch">
      <div class="card w-100 shadow-sm d-flex flex-column justify-content-start">
        <h3 class="mb-4 text-primary p-4"><i class="fas fa-robot me-2"></i>Ashley</h3>
        <div id="chatMessages" class="border rounded p-3 mx-4 mb-3" style="height: 300px; overflow-y: auto; background-color: #f8f9fa;"></div>
        <div class="input-group mx-4 mb-3" style="width: 90%;">
          <input type="text" id="chatInput" class="form-control form-control-lg" placeholder="Ask me anything...">
          <button class="btn btn-primary" id="sendChat">
            <i class="fas fa-paper-plane"></i>
          </button>
        </div>
        <div class="mt-2 mx-4 mb-4">
          <p class="text-muted fw-medium small" style="word-wrap: break-word; overflow-wrap: break-word;">Ashley can help you with:</p>
          <ul class="text-muted small" style="word-wrap: break-word; overflow-wrap: break-word; padding-right: 10px;">
            <li>Checkout process</li>
            <li>Check-in and check-out procedures</li>
            <li>Finding your way around</li>
            <li>General inquiries</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</div>
<!-- Load html5-qrcode from local static directory -->
<script src="/static/js/html5-qrcode.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/js/all.min.js"></script>
<audio id="thankYouAudio" src="/static/audio/thank_you_for_visiting.mp3" preload="auto"></audio>
<script>
document.addEventListener('DOMContentLoaded', function() {
  const startScanBtn = document.getElementById('startScanBtn');
  const qrReader = document.getElementById('qr-reader');
  const tempIdInput = document.getElementById('tempIdInput');
  const checkoutForm = document.querySelector('form[action="/checkout"]');
  const thankYouAudio = document.getElementById('thankYouAudio');
  let html5QrScanner = null;
  let scanInProgress = false;

  function stopScanner() {
    if (html5QrScanner && scanInProgress) {
      scanInProgress = false;
      html5QrScanner.stop().then(() => {
        html5QrScanner.clear().then(() => {
          qrReader.style.display = 'none';
          startScanBtn.disabled = false;
          html5QrScanner = null;
        });
      });
    }
  }

  function speakThankYouAndRedirect() {
    if ('speechSynthesis' in window) {
      const utter = new SpeechSynthesisUtterance('You have been successfully checked out. Thank you for visiting us.');
      utter.onend = function() {
        window.location.href = '/';
      };
      window.speechSynthesis.speak(utter);
    } else {
      // Fallback: just redirect immediately
      window.location.href = '/';
    }
  }

  function ajaxCheckout(tempId) {
    console.log('Attempting AJAX checkout for tempId:', tempId);
    fetch('/checkout', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: `temp_id=${encodeURIComponent(tempId)}`
    })
    .then(async response => {
      let data;
      try {
        data = await response.json();
      } catch (e) {
        console.error('Invalid JSON response:', e, response);
        alert('Server error: Invalid response.');
        return;
      }
      console.log('Checkout response:', data);
      if (data.success) {
        speakThankYouAndRedirect();
      } else {
        alert(data.message || 'Checkout failed. Please try again.');
      }
    })
    .catch((err) => {
      console.error('AJAX checkout error:', err);
      alert('Checkout failed. Please try again.');
    });
  }

  if (startScanBtn && qrReader && tempIdInput && checkoutForm) {
    startScanBtn.addEventListener('click', function() {
      console.log('Scan QR button clicked');
      if (typeof Html5Qrcode === 'undefined') {
        alert('QR scanning library failed to load. Please refresh the page.');
        return;
      }
      Html5Qrcode.getCameras().then(cameras => {
        console.log('Cameras found:', cameras);
        if (cameras && cameras.length) {
          qrReader.style.display = 'block';
          startScanBtn.disabled = true;
          if (!html5QrScanner) {
            html5QrScanner = new Html5Qrcode("qr-reader");
          }
          scanInProgress = true;
          html5QrScanner.start(
            { facingMode: "environment" },
            { fps: 10, qrbox: 250 },
            qrCodeMessage => {
              if (!scanInProgress) return;
              scanInProgress = false;
              console.log('QR code scanned:', qrCodeMessage);
              tempIdInput.value = qrCodeMessage;
              stopScanner();
              console.log('QR scanned, calling ajaxCheckout...');
              ajaxCheckout(qrCodeMessage);
            },
            errorMessage => { if (scanInProgress) console.log('QR scan error:', errorMessage); }
          ).catch(err => {
            alert('Unable to access camera for QR scan.');
            qrReader.style.display = 'none';
            startScanBtn.disabled = false;
            console.log('Camera error:', err);
          });
        } else {
          alert('No camera found on this device.');
          console.log('No camera found');
        }
      }).catch(err => {
        alert('Unable to access camera for QR scan.');
        console.log('Camera access error:', err);
      });
    });
  }
  // Chatbot logic (same as registration)
  const chatInput = document.getElementById('chatInput');
  const sendChat = document.getElementById('sendChat');
  const chatMessages = document.getElementById('chatMessages');
  function addMessage(message, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'd-flex mb-2' + (isUser ? ' justify-content-end' : '');
    if (isUser) {
      messageDiv.innerHTML = `
        <div class="border rounded p-2 chat-message-user" style="max-width: 80%;">
          ${message}
        </div>
        <div class="rounded-circle bg-info text-white p-2 ms-2" style="width: 32px; height: 32px; text-align: center;">
          <i class="fas fa-user"></i>
        </div>
      `;
    } else {
      messageDiv.innerHTML = `
        <div class="rounded-circle bg-primary text-white p-2 me-2" style="width: 32px; height: 32px; text-align: center;">
          <i class="fas fa-robot"></i>
        </div>
        <div class="border rounded p-2 chat-message-bot" style="max-width: 80%;">
          ${message}
        </div>
      `;
    }
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
  if (chatInput && sendChat && chatMessages) {
    addMessage("Hello! I'm Ashley. I can help you with visitor checkout and answer any questions you might have.");
    sendChat.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', function(e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        sendMessage();
      }
    });
  }
  function sendMessage() {
    const message = chatInput.value.trim();
    if (message !== '') {
      addMessage(message, true);
      chatInput.value = '';
      fetch('/api/chatbot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message })
      })
      .then(response => response.json())
      .then(data => {
        addMessage(data.response);
      })
      .catch(error => {
        addMessage('Sorry, I encountered an error. Please try again later.');
      });
    }
  }
});
</script>
<style>
.custom-green-btn {
  background: #28a745 !important;
  color: #fff !important;
  border: none !important;
}
.custom-green-btn:hover, .custom-green-btn:focus {
  background: #218838 !important;
  color: #fff !important;
}
.custom-red-btn {
  background: #dc3545 !important;
  color: #fff !important;
  border: none !important;
}
.custom-red-btn:hover, .custom-red-btn:focus {
  background: #b52a37 !important;
  color: #fff !important;
}
  #qr-reader { max-width: 100%; border: 1px solid #ccc; margin-bottom: 1rem; min-height: 250px; }
  .ai-equal-height { min-height: 520px; }
  @media (min-width: 992px) { .ai-equal-height { height: 100%; } }
  @media (max-width: 991.98px) {
    .flex-lg-row { flex-direction: column !important; }
    .order-1 { order: 1 !important; }
    .order-2 { order: 2 !important; }
    .col-lg-4, .col-lg-8 { max-width: 100%; flex: 0 0 100%; }
    .ai-equal-height { min-height: 0; }
  }
</style>
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
