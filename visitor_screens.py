from flask import render_template_string, url_for, request
from theme import themed
from ai_helpers import generate_purpose_suggestions, get_chatbot_response

VISITOR_FORM = '''
<div class="container-fluid min-vh-100 d-flex flex-column py-4">
  <div class="row flex-grow-1">
    <!-- AI Agent on the left -->
    <div class="col-md-4">
      <div class="card h-100 shadow-sm">
        <h3 class="mb-4 text-primary p-4"><i class="fas fa-robot me-2"></i>Ashley</h3>
        <div id="chatMessages" class="border rounded p-3 mx-4 mb-3" style="height: calc(100% - 300px); overflow-y: auto; background-color: #f8f9fa;">
          <div class="d-flex mb-3">
            <div class="rounded-circle bg-primary text-white p-2 me-2" style="width: 40px; height: 40px; text-align: center;">
              <i class="fas fa-robot"></i>
            </div>
            <div class="border rounded p-3 chat-message-bot" style="max-width: 80%; word-wrap: break-word; overflow-wrap: break-word;">
              <p class="mb-0" style="font-size: 0.95rem;">Hello! I'm Ashley. I can help you with visitor registration and answer any questions you might have.</p>
            </div>
          </div>
        </div>
        <div class="input-group mx-4 mb-3" style="width: 90%;">
          <input type="text" id="chatInput" class="form-control form-control-lg" placeholder="Ask me anything...">
          <button class="btn btn-primary" id="sendChat">
            <i class="fas fa-paper-plane"></i>
          </button>
        </div>
        <div class="mt-2 mx-4 mb-4">
          <p class="text-muted fw-medium small" style="word-wrap: break-word; overflow-wrap: break-word;">Ashley can help you with:</p>
          <ul class="text-muted small" style="word-wrap: break-word; overflow-wrap: break-word; padding-right: 10px;">
            <li>Visitor registration process</li>
            <li>Check-in and check-out procedures</li>
            <li>Finding your way around</li>
            <li>General inquiries</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Registration form on the right -->
    <div class="col-md-8">
      <div class="card h-100 shadow-sm">
        <div class="card-header bg-primary text-white p-4">
          <h2 class="mb-0">Visitor Registration</h2>
        </div>
        <div class="card-body p-4">
          <form method="post" action="/register">
            <div class="row">
              <div class="col-md-6 mb-3">
                <label class="form-label fw-medium">Name:</label>
                <input class="form-control form-control-lg" type="text" name="name" id="visitorName" required>
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label fw-medium">Email:</label>
                <input class="form-control form-control-lg" type="email" name="email" required>
              </div>
            </div>
            <div class="row">
              <div class="col-md-6 mb-3">
                <label class="form-label fw-medium">Phone:</label>
                <input class="form-control form-control-lg" type="text" name="phone" required>
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label fw-medium">Company:</label>
                <input class="form-control form-control-lg" type="text" name="company" id="companyInput" required>
              </div>
            </div>
            <div class="mb-3">
              <label class="form-label fw-medium">Purpose of Visit:</label>
              <input class="form-control form-control-lg" type="text" name="purpose" id="purposeInput" required>
              <div id="purposeSuggestions" class="mt-2" style="display:none;">
                <p class="mb-1 text-muted fw-medium small">AI Suggestions:</p>
                <div id="suggestionButtons" class="d-flex flex-wrap gap-1"></div>
              </div>
            </div>
            <div class="mb-3">
              <label class="form-label fw-medium">Whom to Meet:</label>
              <input class="form-control form-control-lg" type="text" name="whom_to_meet" required>
            </div>
            <div class="d-grid gap-2">
              <button class="btn btn-primary btn-lg btn-raised" type="submit">
                <i class="fas fa-user-plus me-2"></i>Register
              </button>
              <a class="btn btn-danger btn-lg btn-raised" href="/checkout">
                <i class="fas fa-sign-out-alt me-2"></i>Check Out
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
<script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/js/all.min.js"></script>
<script>
  document.addEventListener('DOMContentLoaded', function() {
    // Purpose suggestions based on company
    const companyInput = document.getElementById('companyInput');
    const purposeInput = document.getElementById('purposeInput');
    const purposeSuggestions = document.getElementById('purposeSuggestions');
    const suggestionButtons = document.getElementById('suggestionButtons');

    companyInput.addEventListener('blur', function() {
      if (companyInput.value.trim() !== '') {
        // Fetch purpose suggestions from the server
        fetch('/api/purpose-suggestions?company=' + encodeURIComponent(companyInput.value))
          .then(response => response.json())
          .then(data => {
            suggestionButtons.innerHTML = '';
            if (data.suggestions && data.suggestions.length > 0) {
              data.suggestions.forEach(suggestion => {
                const btn = document.createElement('button');
                btn.type = 'button';
                btn.className = 'btn btn-sm btn-outline-primary mb-1';
                btn.textContent = suggestion;
                btn.addEventListener('click', function() {
                  purposeInput.value = suggestion;
                });
                suggestionButtons.appendChild(btn);
              });
              purposeSuggestions.style.display = 'block';
            }
          })
          .catch(error => console.error('Error fetching suggestions:', error));
      }
    });

    // Chatbot functionality
    const chatInput = document.getElementById('chatInput');
    const sendChat = document.getElementById('sendChat');
    const chatMessages = document.getElementById('chatMessages');
    const visitorName = document.getElementById('visitorName');

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

    function sendMessage() {
      const message = chatInput.value.trim();
      if (message !== '') {
        addMessage(message, true);
        chatInput.value = '';

        // Get visitor name if available
        const name = visitorName.value.trim();

        // Send message to server
        fetch('/api/chatbot', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            message: message,
            visitor_name: name
          }),
        })
        .then(response => response.json())
        .then(data => {
          addMessage(data.response);
        })
        .catch(error => {
          console.error('Error:', error);
          addMessage('Sorry, I encountered an error. Please try again later.');
        });
      }
    }

    sendChat.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', function(e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        sendMessage();
      }
    });
  });
</script>
'''

def render_visitor_form():
    return render_template_string(themed(VISITOR_FORM))

QR_DISPLAY = '''
<div class="container-fluid min-vh-100 d-flex flex-column py-4">
  <div class="row flex-grow-1">
    <!-- AI Agent on the left -->
    <div class="col-md-4">
      <div class="card h-100 shadow-sm">
        <h3 class="mb-4 text-primary p-4"><i class="fas fa-robot me-2"></i>Ashley</h3>
        <div id="chatMessages" class="border rounded p-3 mx-4 mb-3" style="height: calc(100% - 300px); overflow-y: auto; background-color: #f8f9fa;">
          <div class="d-flex mb-3">
            <div class="rounded-circle bg-primary text-white p-2 me-2" style="width: 40px; height: 40px; text-align: center;">
              <i class="fas fa-robot"></i>
            </div>
            <div class="border rounded p-3 chat-message-bot" style="max-width: 80%; word-wrap: break-word; overflow-wrap: break-word;">
              <p class="mb-0" style="font-size: 0.95rem;">Thank you for registering! I can help you with the check-in process. Simply scan your QR code at the check-in counter.</p>
            </div>
          </div>
        </div>
        <div class="input-group mx-4 mb-3" style="width: 90%;">
          <input type="text" id="chatInput" class="form-control form-control-lg" placeholder="Ask me anything...">
          <button class="btn btn-primary" id="sendChat">
            <i class="fas fa-paper-plane"></i>
          </button>
        </div>
        <div class="mt-2 mx-4 mb-4">
          <p class="text-muted fw-medium small" style="word-wrap: break-word; overflow-wrap: break-word;">Ashley can help you with:</p>
          <ul class="text-muted small" style="word-wrap: break-word; overflow-wrap: break-word; padding-right: 10px;">
            <li>Check-in procedures</li>
            <li>Finding your way around</li>
            <li>General inquiries</li>
            <li>Information about our facilities</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- QR Code display on the right -->
    <div class="col-md-8">
      <div class="card h-100 shadow-sm">
        <div class="card-header bg-success text-white p-4">
          <h2 class="mb-0">Registration Successful</h2>
        </div>
        <div class="card-body p-4 text-center">
          <div class="row">
            <div class="col-md-6">
              <div class="card mb-3 shadow-sm">
                <div class="card-body">
                  <h4 class="card-title">Visitor Information</h4>
                  <div class="mb-2">
                    <span class="text-muted fw-medium">Name:</span>
                    <span class="fw-bold">{{ name }}</span>
                  </div>
                  <div class="mb-2">
                    <span class="text-muted fw-medium">Company:</span>
                    <span class="fw-bold">{{ company }}</span>
                  </div>
                  <div class="mb-2">
                    <span class="text-muted fw-medium">Temporary ID:</span>
                    <span class="fw-bold">{{ temp_id }}</span>
                  </div>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="card mb-3 shadow-sm">
                <div class="card-body">
                  <h4 class="card-title">Your QR Code</h4>
                  <img src="{{ url_for('qr_code', temp_id=temp_id) }}" alt="QR Code" class="img-fluid mb-3 border p-2" id="qrCodeImage">
                  <p class="small text-muted fw-medium">Scan this QR code at the <a href="/checkin" class="fw-bold">Check-In</a> counter</p>
                  <div class="btn-group mt-3 w-100">
                    <button class="btn btn-sm btn-outline-primary" id="downloadQRBtn">
                      <i class="fas fa-download me-1"></i> Download
                    </button>
                    <button class="btn btn-sm btn-outline-secondary" id="printQRBtn">
                      <i class="fas fa-print me-1"></i> Print
                    </button>
                    <button class="btn btn-sm btn-outline-success" id="shareQRBtn">
                      <i class="fas fa-share-alt me-1"></i> Share
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="d-grid gap-2 col-md-8 mx-auto mt-4">
            <a class="btn btn-outline-primary btn-lg btn-raised" href="/">
              <i class="fas fa-arrow-left me-2"></i>Back to Registration
            </a>
            <a class="btn btn-danger btn-lg btn-raised" href="/checkout">
              <i class="fas fa-sign-out-alt me-2"></i>Check Out
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/js/all.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
<script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>
<script>
  // Ensure buttons are properly initialized
  document.addEventListener('DOMContentLoaded', function() {
    // Add event listeners to buttons
    const downloadQRBtn = document.getElementById('downloadQRBtn');
    if (downloadQRBtn) {
      downloadQRBtn.addEventListener('click', downloadQRCode);
    }

    const printQRBtn = document.getElementById('printQRBtn');
    if (printQRBtn) {
      printQRBtn.addEventListener('click', printQRCode);
    }

    const shareQRBtn = document.getElementById('shareQRBtn');
    if (shareQRBtn) {
      shareQRBtn.addEventListener('click', shareQRCode);
    }

    console.log('QR code buttons initialized');
  });

  // QR Code functions
  function downloadQRCode() {
    const qrCodeImg = document.getElementById('qrCodeImage');

    // Check if QR code image exists
    if (!qrCodeImg) {
      console.error('QR code image not found');
      alert('Error: QR code image not found');
      return;
    }

    const qrCodeUrl = qrCodeImg.src;

    // Check if QR code URL is valid
    if (!qrCodeUrl || qrCodeUrl === '') {
      console.error('QR code URL is empty or invalid');
      alert('Error: QR code image is not properly loaded');
      return;
    }

    // Get visitor information
    const nameLabel = Array.from(document.querySelectorAll('.text-muted')).find(el => el.textContent.includes('Name:'));
    const visitorName = nameLabel ? nameLabel.nextElementSibling.textContent : 'Visitor';

    const companyLabel = Array.from(document.querySelectorAll('.text-muted')).find(el => el.textContent.includes('Company:'));
    const visitorCompany = companyLabel ? companyLabel.nextElementSibling.textContent : '';

    const idLabel = Array.from(document.querySelectorAll('.text-muted')).find(el => el.textContent.includes('Temporary ID:'));
    const visitorId = idLabel ? idLabel.nextElementSibling.textContent.trim() : '';

    // Create a filename with visitor ID if available
    const filename = visitorId ? `idcard_${visitorId}.png` : 'idcard.png';

    // Show download indicator
    const downloadBtn = document.getElementById('downloadQRBtn');
    if (!downloadBtn) {
      console.warn('Download button not found');
    }
    const originalContent = downloadBtn ? downloadBtn.innerHTML : '';
    if (downloadBtn) {
      downloadBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i> Downloading...';
      downloadBtn.disabled = true;
    }

    try {
      // Create an ID card as HTML
      const idCardHtml = `
        <div class="id-card" style="width: 400px; margin: 0 auto; border: 1px solid #ddd; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 8px rgba(0,0,0,0.1); background-color: white;">
          <div class="id-card-header" style="background-color: #0d6efd; color: white; padding: 15px; text-align: center;">
            <h3>VISITOR ID CARD</h3>
          </div>
          <div class="id-card-body" style="padding: 20px;">
            <div class="visitor-info" style="margin-bottom: 20px;">
              <div class="info-row" style="margin-bottom: 10px; display: flex;">
                <div class="info-label" style="font-weight: 500; width: 100px;">Name:</div>
                <div class="info-value" style="font-weight: 600; flex: 1;">${visitorName}</div>
              </div>
              <div class="info-row" style="margin-bottom: 10px; display: flex;">
                <div class="info-label" style="font-weight: 500; width: 100px;">Company:</div>
                <div class="info-value" style="font-weight: 600; flex: 1;">${visitorCompany}</div>
              </div>
              <div class="info-row" style="margin-bottom: 10px; display: flex;">
                <div class="info-label" style="font-weight: 500; width: 100px;">ID Number:</div>
                <div class="info-value" style="font-weight: 600; flex: 1;">${visitorId}</div>
              </div>
            </div>
            <div class="qr-container" style="text-align: center; padding: 10px; border-top: 1px solid #eee;">
              <img src="${qrCodeUrl}" alt="QR Code" style="max-width: 180px; margin-bottom: 8px; border: 1px solid #ddd; padding: 8px;">
              <p style="font-size: 12px; color: #6c757d;">Scan this QR code at the Check-In counter</p>
            </div>
          </div>
        </div>
      `;

      // Create a temporary container to render the ID card
      const container = document.createElement('div');
      container.innerHTML = idCardHtml;
      container.style.position = 'absolute';
      container.style.left = '-9999px';
      document.body.appendChild(container);

      // Find the image in the container and set crossOrigin
      const containerImg = container.querySelector('img');
      containerImg.crossOrigin = "anonymous";

      // Function to process the image once it's loaded
      function processLoadedImage() {
        // Give the browser a moment to fully render the container
        setTimeout(() => {
          // Once image is loaded, proceed with html2canvas
          html2canvas(container.querySelector('.id-card'), {
            allowTaint: true,
            useCORS: true,
            logging: false,
            backgroundColor: null
          }).then(canvas => {
            // Convert canvas to data URL
            const dataUrl = canvas.toDataURL('image/png');

            // Create a temporary link element
            const downloadLink = document.createElement('a');
            downloadLink.href = dataUrl;
            downloadLink.download = filename;

            // Append to the document, click it, and remove it
            document.body.appendChild(downloadLink);
            downloadLink.click();
            document.body.removeChild(downloadLink);
            document.body.removeChild(container);

            // Show success message
            if (downloadBtn) {
              setTimeout(() => {
                downloadBtn.innerHTML = '<i class="fas fa-check me-1"></i> Downloaded';
                setTimeout(() => {
                  downloadBtn.innerHTML = originalContent;
                  downloadBtn.disabled = false;
                }, 1500);
              }, 500);
            }
          }).catch(error => {
            console.error('ID card generation failed:', error);
            alert('Download failed. Please try again.');
            if (downloadBtn) {
              downloadBtn.innerHTML = originalContent;
              downloadBtn.disabled = false;
            }
            document.body.removeChild(container);
          });
        }, 100); // 100ms delay to ensure DOM is ready
      }

      // Handle image loading error
      containerImg.onerror = function() {
        console.error('Failed to load QR code image');
        alert('Failed to load QR code image. Please try again.');
        if (downloadBtn) {
          downloadBtn.innerHTML = originalContent;
          downloadBtn.disabled = false;
        }
        document.body.removeChild(container);
      };

      // Set up the onload handler
      containerImg.onload = processLoadedImage;

      // Check if the image is already loaded
      if (containerImg.complete) {
        processLoadedImage();
      }

    } catch (error) {
      console.error('Download failed:', error);
      alert('Download failed. Please try again.');
      if (downloadBtn) {
        downloadBtn.innerHTML = originalContent;
        downloadBtn.disabled = false;
      }
    }
  }

  function printQRCode() {
    const qrCodeImg = document.getElementById('qrCodeImage');

    // Check if QR code image exists
    if (!qrCodeImg) {
      console.error('QR code image not found');
      alert('Error: QR code image not found');
      return;
    }

    const qrCodeUrl = qrCodeImg.src;

    // Check if QR code URL is valid
    if (!qrCodeUrl || qrCodeUrl === '') {
      console.error('QR code URL is empty or invalid');
      alert('Error: QR code image is not properly loaded');
      return;
    }

    // Show print indicator
    const printBtn = document.getElementById('printQRBtn');
    if (!printBtn) {
      console.warn('Print button not found');
    }
    const originalContent = printBtn ? printBtn.innerHTML : '';
    if (printBtn) {
      printBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i> Preparing...';
      printBtn.disabled = true;
    }

    try {
      // Get visitor information
      const nameLabel = Array.from(document.querySelectorAll('.text-muted')).find(el => el.textContent.includes('Name:'));
      const visitorName = nameLabel ? nameLabel.nextElementSibling.textContent : 'Visitor';

      const companyLabel = Array.from(document.querySelectorAll('.text-muted')).find(el => el.textContent.includes('Company:'));
      const visitorCompany = companyLabel ? companyLabel.nextElementSibling.textContent : '';

      const idLabel = Array.from(document.querySelectorAll('.text-muted')).find(el => el.textContent.includes('Temporary ID:'));
      const visitorId = idLabel ? idLabel.nextElementSibling.textContent : '';

      // Create a new window with formatted visitor info and QR code
      const printWindow = window.open('', '_blank');
      if (!printWindow) {
        throw new Error('Could not open print window. Please check if pop-ups are blocked.');
      }

      printWindow.document.write(
        '<!DOCTYPE html>' +
        '<html>' +
        '<head>' +
          '<title>Visitor ID Card</title>' +
          '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">' +
          '<style>' +
            'body { padding: 20px; background-color: #f8f9fa; }' +
            '.id-card { max-width: 400px; margin: 0 auto; border: 1px solid #ddd; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 8px rgba(0,0,0,0.1); background-color: white; }' +
            '.id-card-header { background-color: #0d6efd; color: white; padding: 15px; text-align: center; }' +
            '.id-card-body { padding: 20px; }' +
            '.visitor-info { margin-bottom: 20px; }' +
            '.info-row { margin-bottom: 10px; display: flex; }' +
            '.info-label { font-weight: 500; width: 100px; }' +
            '.info-value { font-weight: 600; flex: 1; }' +
            '.qr-container { text-align: center; padding: 10px; border-top: 1px solid #eee; }' +
            '@media print { body { background-color: white; } .id-card { box-shadow: none; border: 1px solid #ddd; } }' +
          '</style>' +
        '</head>' +
        '<body>' +
          '<div class="id-card">' +
            '<div class="id-card-header">' +
              '<h3>VISITOR ID CARD</h3>' +
            '</div>' +
            '<div class="id-card-body">' +
              '<div class="visitor-info">' +
                '<div class="info-row">' +
                  '<div class="info-label">Name:</div>' +
                  '<div class="info-value">' + visitorName + '</div>' +
                '</div>' +
                '<div class="info-row">' +
                  '<div class="info-label">Company:</div>' +
                  '<div class="info-value">' + visitorCompany + '</div>' +
                '</div>' +
                '<div class="info-row">' +
                  '<div class="info-label">ID Number:</div>' +
                  '<div class="info-value">' + visitorId + '</div>' +
                '</div>' +
              '</div>' +
              '<div class="qr-container">' +
                '<img src="' + qrCodeUrl + '" alt="QR Code" class="img-fluid mb-2 border p-2" style="max-width: 180px;">' +
                '<p class="small text-muted">Scan this QR code at the Check-In counter</p>' +
              '</div>' +
            '</div>' +
          '</div>' +
          '<script>' +
            'window.onload = function() { window.print(); window.opener.postMessage("print-completed", "*"); };' +
          '<\/script>' +
        '</body>' +
        '</html>'
      );
      printWindow.document.close();

      // Listen for message from print window
      window.addEventListener('message', function printMessageHandler(event) {
        if (event.data === 'print-completed') {
          // Remove the event listener to avoid memory leaks
          window.removeEventListener('message', printMessageHandler);

          // Show success message
          if (printBtn) {
            printBtn.innerHTML = '<i class="fas fa-check me-1"></i> Printed';
            setTimeout(() => {
              printBtn.innerHTML = originalContent;
              printBtn.disabled = false;
            }, 1500);
          }
        }
      }, { once: true });

      // Fallback in case the message is not received
      setTimeout(() => {
        if (printBtn && printBtn.disabled) {
          printBtn.innerHTML = originalContent;
          printBtn.disabled = false;
        }
      }, 5000);

    } catch (error) {
      console.error('Print failed:', error);
      alert('Print failed: ' + error.message);
      if (printBtn) {
        printBtn.innerHTML = originalContent;
        printBtn.disabled = false;
      }
    }
  }

  function shareQRCode() {
    // Show share indicator on the button
    const shareBtn = document.getElementById('shareQRBtn');
    if (!shareBtn) {
      console.warn('Share button not found');
    }
    const originalContent = shareBtn ? shareBtn.innerHTML : '';
    if (shareBtn) {
      shareBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i> Preparing...';
      shareBtn.disabled = true;
    }

    try {
      const qrCodeImg = document.getElementById('qrCodeImage');

      // Check if QR code image exists
      if (!qrCodeImg) {
        throw new Error('QR code image not found');
      }

      const qrCodeUrl = qrCodeImg.src;

      // Check if QR code URL is valid
      if (!qrCodeUrl || qrCodeUrl === '') {
        throw new Error('QR code image is not properly loaded');
      }

      // Get visitor information
      const nameLabel = Array.from(document.querySelectorAll('.text-muted')).find(el => el.textContent.includes('Name:'));
      const visitorName = nameLabel ? nameLabel.nextElementSibling.textContent : 'Visitor';

      const companyLabel = Array.from(document.querySelectorAll('.text-muted')).find(el => el.textContent.includes('Company:'));
      const visitorCompany = companyLabel ? companyLabel.nextElementSibling.textContent : '';

      const idLabel = Array.from(document.querySelectorAll('.text-muted')).find(el => el.textContent.includes('Temporary ID:'));
      const visitorId = idLabel ? idLabel.nextElementSibling.textContent.trim() : '';

      // Create an ID card as HTML
      const idCardHtml = `
        <div class="id-card" style="width: 400px; margin: 0 auto; border: 1px solid #ddd; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 8px rgba(0,0,0,0.1); background-color: white;">
          <div class="id-card-header" style="background-color: #0d6efd; color: white; padding: 15px; text-align: center;">
            <h3>VISITOR ID CARD</h3>
          </div>
          <div class="id-card-body" style="padding: 20px;">
            <div class="visitor-info" style="margin-bottom: 20px;">
              <div class="info-row" style="margin-bottom: 10px; display: flex;">
                <div class="info-label" style="font-weight: 500; width: 100px;">Name:</div>
                <div class="info-value" style="font-weight: 600; flex: 1;">${visitorName}</div>
              </div>
              <div class="info-row" style="margin-bottom: 10px; display: flex;">
                <div class="info-label" style="font-weight: 500; width: 100px;">Company:</div>
                <div class="info-value" style="font-weight: 600; flex: 1;">${visitorCompany}</div>
              </div>
              <div class="info-row" style="margin-bottom: 10px; display: flex;">
                <div class="info-label" style="font-weight: 500; width: 100px;">ID Number:</div>
                <div class="info-value" style="font-weight: 600; flex: 1;">${visitorId}</div>
              </div>
            </div>
            <div class="qr-container" style="text-align: center; padding: 10px; border-top: 1px solid #eee;">
              <img src="${qrCodeUrl}" alt="QR Code" style="max-width: 180px; margin-bottom: 8px; border: 1px solid #ddd; padding: 8px;">
              <p style="font-size: 12px; color: #6c757d;">Scan this QR code at the Check-In counter</p>
            </div>
          </div>
        </div>
      `;

      // Create a temporary container to render the ID card
      const container = document.createElement('div');
      container.innerHTML = idCardHtml;
      container.style.position = 'absolute';
      container.style.left = '-9999px';
      document.body.appendChild(container);

      // Find the image in the container and set crossOrigin
      const containerImg = container.querySelector('img');
      containerImg.crossOrigin = "anonymous";

      // Wait for the image in the container to load
      containerImg.onload = function() {
        // Once image is loaded, proceed with html2canvas
        html2canvas(container.firstChild, {
          allowTaint: true,
          useCORS: true
        }).then(canvas => {
          // Convert canvas to data URL
          const idCardImageUrl = canvas.toDataURL('image/png');
          document.body.removeChild(container);

          // Create a modal for sharing options
          const modal = document.createElement('div');
          modal.className = 'modal fade';
          modal.id = 'shareModal';
          modal.setAttribute('tabindex', '-1');
          modal.setAttribute('aria-labelledby', 'shareModalLabel');
          modal.setAttribute('aria-hidden', 'true');
          modal.innerHTML = 
            '<div class="modal-dialog">' +
            '<div class="modal-content">' +
            '<div class="modal-header">' +
            '<h5 class="modal-title" id="shareModalLabel">Share ID Card</h5>' +
            '<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>' +
            '</div>' +
            '<div class="modal-body">' +
            '<div class="text-center mb-3">' +
            '<img src="' + idCardImageUrl + '" alt="ID Card" class="img-fluid mb-2 border p-2" style="max-width: 300px;">' +
            '<p class="small text-muted">ID Card for ' + visitorName + (visitorId ? ' (ID: ' + visitorId + ')' : '') + '</p>' +
            '</div>' +
            '<div class="d-grid gap-2">' +
            '<button class="btn btn-success" id="whatsappShareBtn">' +
            '<i class="fab fa-whatsapp me-2"></i>Share via WhatsApp' +
            '</button>' +
            '<button class="btn btn-primary" id="bluetoothShareBtn">' +
            '<i class="fab fa-bluetooth-b me-2"></i>Share via Bluetooth' +
            '</button>' +
            '<button class="btn btn-secondary" id="otherShareBtn">' +
            '<i class="fas fa-share-alt me-2"></i>Other Sharing Options' +
            '</button>' +
            '</div>' +
            '</div>' +
            '</div>' +
            '</div>';

          document.body.appendChild(modal);

          // Add event listeners to share buttons
          document.getElementById('whatsappShareBtn').addEventListener('click', function() {
            shareViaWhatsApp(idCardImageUrl);
          });

          document.getElementById('bluetoothShareBtn').addEventListener('click', function() {
            shareViaBluetooth(idCardImageUrl);
          });

          document.getElementById('otherShareBtn').addEventListener('click', function() {
            shareViaOther(idCardImageUrl);
          });

          // Initialize and show the modal
          const shareModal = new bootstrap.Modal(document.getElementById('shareModal'));
          if (!shareModal) {
            throw new Error('Could not create share modal');
          }

          shareModal.show();

          // Remove modal from DOM after it's hidden
          document.getElementById('shareModal').addEventListener('hidden.bs.modal', function () {
            document.body.removeChild(modal);

            // Restore the button state after modal is closed
            if (shareBtn) {
              shareBtn.innerHTML = originalContent;
              shareBtn.disabled = false;
            }
          });
        }).catch(error => {
          console.error('ID card generation failed:', error);
          alert('Sharing failed. Please try again.');
          if (shareBtn) {
            shareBtn.innerHTML = originalContent;
            shareBtn.disabled = false;
          }
          document.body.removeChild(container);
        });
      };

      // Set the image source to trigger loading (if not already loaded)
      if (containerImg.complete) {
        containerImg.onload();
      } else {
        // Handle image loading error
        containerImg.onerror = function() {
          console.error('Failed to load QR code image');
          alert('Failed to load QR code image. Please try again.');
          if (shareBtn) {
            shareBtn.innerHTML = originalContent;
            shareBtn.disabled = false;
          }
          document.body.removeChild(container);
        };
      }
    } catch (error) {
      console.error('Share preparation failed:', error);
      alert('Share preparation failed: ' + error.message);
      if (shareBtn) {
        shareBtn.innerHTML = originalContent;
        shareBtn.disabled = false;
      }
    }
  }

  function shareViaWhatsApp(idCardImageUrl) {
    try {
      // Get visitor information for more personalized sharing
      const nameLabel = Array.from(document.querySelectorAll('.text-muted')).find(el => el.textContent.includes('Name:'));
      const visitorName = nameLabel ? nameLabel.nextElementSibling.textContent.trim() : 'Visitor';

      const idLabel = Array.from(document.querySelectorAll('.text-muted')).find(el => el.textContent.includes('Temporary ID:'));
      const visitorId = idLabel ? idLabel.nextElementSibling.textContent.trim() : '';

      // Create a more descriptive message
      const text = 'Hello! This is ' + visitorName + (visitorId ? ' (ID: ' + visitorId + ')' : '') + 
                   '. Here is my visitor ID card with QR code for check-in: ' + window.location.href;

      const whatsappUrl = 'https://wa.me/?text=' + encodeURIComponent(text);
      const shareWindow = window.open(whatsappUrl, '_blank');

      if (!shareWindow) {
        throw new Error('Could not open WhatsApp sharing. Please check if pop-ups are blocked.');
      }

      // Show success message in the console
      console.log('Shared via WhatsApp successfully');

      // Close the modal
      const shareModal = bootstrap.Modal.getInstance(document.getElementById('shareModal'));
      if (shareModal) {
        shareModal.hide();
      }
    } catch (error) {
      console.error('WhatsApp sharing failed:', error);
      alert('WhatsApp sharing failed: ' + error.message);

      // Keep the modal open if there was an error
    }
  }

  function shareViaBluetooth(idCardImageUrl) {
    try {
      // Check if Web Bluetooth API is supported
      if (!('bluetooth' in navigator)) {
        throw new Error('Bluetooth sharing is not supported by your browser. Please try another sharing method.');
      }

      // Show a message before the Bluetooth device selection dialog
      alert('Please select a Bluetooth device to share with in the next dialog.');

      // Update button to show progress
      const bluetoothBtn = document.getElementById('bluetoothShareBtn');
      if (bluetoothBtn) {
        const originalContent = bluetoothBtn.innerHTML;
        bluetoothBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Connecting...';
        bluetoothBtn.disabled = true;

        // Restore button after 5 seconds if the process takes too long
        setTimeout(() => {
          if (bluetoothBtn.disabled) {
            bluetoothBtn.innerHTML = originalContent;
            bluetoothBtn.disabled = false;
          }
        }, 5000);
      }

      navigator.bluetooth.requestDevice({
        acceptAllDevices: true
      })
      .then(device => {
        // Restore button state
        if (bluetoothBtn) {
          bluetoothBtn.innerHTML = '<i class="fab fa-bluetooth-b me-2"></i>Share via Bluetooth';
          bluetoothBtn.disabled = false;
        }

        alert('Selected device: ' + (device.name || 'Unknown device') + '. Due to browser security restrictions, direct file transfer via Bluetooth requires a native app integration.');

        // Close the modal
        const shareModal = bootstrap.Modal.getInstance(document.getElementById('shareModal'));
        if (shareModal) {
          shareModal.hide();
        }
      })
      .catch(error => {
        console.error('Bluetooth error:', error);

        // Restore button state
        if (bluetoothBtn) {
          bluetoothBtn.innerHTML = '<i class="fab fa-bluetooth-b me-2"></i>Share via Bluetooth';
          bluetoothBtn.disabled = false;
        }

        alert('Could not connect to Bluetooth device: ' + error.message + '. Please try another sharing method.');
      });
    } catch (error) {
      console.error('Bluetooth sharing failed:', error);
      alert('Bluetooth sharing failed: ' + error.message);

      // Keep the modal open if there was an error
    }
  }


  function shareViaOther(idCardImageUrl) {
    try {
      // Get visitor information for more personalized sharing
      const nameLabel = Array.from(document.querySelectorAll('.text-muted')).find(el => el.textContent.includes('Name:'));
      const visitorName = nameLabel ? nameLabel.nextElementSibling.textContent.trim() : 'Visitor';

      const idLabel = Array.from(document.querySelectorAll('.text-muted')).find(el => el.textContent.includes('Temporary ID:'));
      const visitorId = idLabel ? idLabel.nextElementSibling.textContent.trim() : '';

      // Update button to show progress
      const otherBtn = document.getElementById('otherShareBtn');
      if (otherBtn) {
        const originalContent = otherBtn.innerHTML;
        otherBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Sharing...';
        otherBtn.disabled = true;

        // Restore button after 5 seconds if the process takes too long
        setTimeout(() => {
          if (otherBtn.disabled) {
            otherBtn.innerHTML = originalContent;
            otherBtn.disabled = false;
          }
        }, 5000);
      }

      // Check if Web Share API is supported
      if (navigator.share) {
        // Create a file from the ID card image URL if provided
        let shareData = {
          title: 'ID Card for ' + visitorName + (visitorId ? ' (ID: ' + visitorId + ')' : ''),
          text: 'Hello! This is ' + visitorName + (visitorId ? ' (ID: ' + visitorId + ')' : '') + 
                '. Here is my visitor ID card with QR code for check-in.',
          url: window.location.href
        };

        // If ID card image URL is provided and the browser supports sharing files
        if (idCardImageUrl && navigator.canShare && navigator.canShare({ files: [new File([new Blob()], 'test.txt')] })) {
          // Fetch the image and convert it to a file
          fetch(idCardImageUrl)
            .then(res => res.blob())
            .then(blob => {
              const file = new File([blob], 'idcard_' + (visitorId || 'visitor') + '.png', { type: 'image/png' });
              shareData.files = [file];
              return navigator.share(shareData);
            })
            .then(() => {
              console.log('Shared successfully with image');

              // Restore button state
              if (otherBtn) {
                otherBtn.innerHTML = '<i class="fas fa-share-alt me-2"></i>Other Sharing Options';
                otherBtn.disabled = false;
              }

              // Close the modal
              const shareModal = bootstrap.Modal.getInstance(document.getElementById('shareModal'));
              if (shareModal) {
                shareModal.hide();
              }
            })
            .catch(error => {
              console.error('Share with image failed:', error);
              // Fall back to sharing without the image
              return navigator.share(shareData);
            });
        } else {
          // Share without the image if not supported
          navigator.share(shareData)
          .then(() => {
            console.log('Shared successfully');

            // Restore button state
            if (otherBtn) {
              otherBtn.innerHTML = '<i class="fas fa-share-alt me-2"></i>Other Sharing Options';
              otherBtn.disabled = false;
            }

            // Close the modal
            const shareModal = bootstrap.Modal.getInstance(document.getElementById('shareModal'));
            if (shareModal) {
              shareModal.hide();
            }
          })
          .catch(error => {
            console.error('Error sharing:', error);

            // Restore button state
            if (otherBtn) {
              otherBtn.innerHTML = '<i class="fas fa-share-alt me-2"></i>Other Sharing Options';
              otherBtn.disabled = false;
            }

            alert('Could not share the QR code: ' + error.message + '. Please try another method.');
          });
      } }else {
        // Fallback for browsers that don't support Web Share API
        const shareText = 'Hello! This is ' + visitorName + (visitorId ? ' (ID: ' + visitorId + ')' : '') + 
                         '. Here is my visitor QR code for check-in: ' + window.location.href;

        // Restore button state
        if (otherBtn) {
          otherBtn.innerHTML = '<i class="fas fa-share-alt me-2"></i>Other Sharing Options';
          otherBtn.disabled = false;
        }

        const copied = prompt('Copy this text to share your QR code:', shareText);

        // Close the modal if the user clicked OK on the prompt
        if (copied !== null) {
          const shareModal = bootstrap.Modal.getInstance(document.getElementById('shareModal'));
          if (shareModal) {
            shareModal.hide();
          }
        }
      }
    } catch (error) {
      console.error('Sharing failed:', error);
      alert('Sharing failed: ' + error.message);

      // Restore button state for the "Other" button
      const otherBtn = document.getElementById('otherShareBtn');
      if (otherBtn) {
        otherBtn.innerHTML = '<i class="fas fa-share-alt me-2"></i>Other Sharing Options';
        otherBtn.disabled = false;
      }

      // Keep the modal open if there was an error
    }
  }

  document.addEventListener('DOMContentLoaded', function() {
    // Chatbot functionality
    const chatInput = document.getElementById('chatInput');
    const sendChat = document.getElementById('sendChat');
    const chatMessages = document.getElementById('chatMessages');

    function addMessage(message, isUser = false) {
      const messageDiv = document.createElement('div');
      messageDiv.className = 'd-flex mb-2' + (isUser ? ' justify-content-end' : '');

      if (isUser) {
        messageDiv.innerHTML = 
          '<div class="border rounded p-2 chat-message-user" style="max-width: 80%;">' +
            message +
          '</div>' +
          '<div class="rounded-circle bg-info text-white p-2 ms-2" style="width: 32px; height: 32px; text-align: center;">' +
            '<i class="fas fa-user"></i>' +
          '</div>';
      } else {
        messageDiv.innerHTML = 
          '<div class="rounded-circle bg-primary text-white p-2 me-2" style="width: 32px; height: 32px; text-align: center;">' +
            '<i class="fas fa-robot"></i>' +
          '</div>' +
          '<div class="border rounded p-2 chat-message-bot" style="max-width: 80%;">' +
            message +
          '</div>';
      }

      chatMessages.appendChild(messageDiv);
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function sendMessage() {
      const message = chatInput.value.trim();
      if (message !== '') {
        addMessage(message, true);
        chatInput.value = '';

        // Get visitor name from the page
        const nameLabel = Array.from(document.querySelectorAll('.text-muted')).find(el => el.textContent.includes('Name:'));
        const visitorName = nameLabel ? nameLabel.nextElementSibling.textContent : '';

        // Send message to server
        fetch('/api/chatbot', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            message: message,
            visitor_name: visitorName
          }),
        })
        .then(response => response.json())
        .then(data => {
          addMessage(data.response);
        })
        .catch(error => {
          console.error('Error:', error);
          addMessage('Sorry, I encountered an error. Please try again later.');
        });
      }
    }

    sendChat.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', function(e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        sendMessage();
      }
    });
  });
</script>
'''

def render_qr_display(name, company, temp_id):
    # Ensure all JavaScript is properly enclosed in script tags
    from markupsafe import Markup
    # Mark the QR_DISPLAY as safe to prevent auto-escaping
    safe_display = Markup(themed(QR_DISPLAY))
    return render_template_string(safe_display, name=name, company=company, temp_id=temp_id)

CHECKOUT_FORM = '''
<div class="container-fluid min-vh-100 d-flex flex-column py-4">
  <div class="row flex-grow-1">
    <!-- AI Agent on the left -->
    <div class="col-md-4">
      <div class="card h-100 shadow-sm">
        <h3 class="mb-4 text-primary p-4"><i class="fas fa-robot me-2"></i>Ashley</h3>
        <div id="chatMessages" class="border rounded p-3 mx-4 mb-3" style="height: calc(100% - 300px); overflow-y: auto; background-color: #f8f9fa;">
          <div class="d-flex mb-3">
            <div class="rounded-circle bg-primary text-white p-2 me-2" style="width: 40px; height: 40px; text-align: center;">
              <i class="fas fa-robot"></i>
            </div>
            <div class="border rounded p-3 chat-message-bot" style="max-width: 80%; word-wrap: break-word; overflow-wrap: break-word;">
              <p class="mb-0" style="font-size: 0.95rem;">Hello! I'm Ashley. I can help you with the checkout process. Simply scan your QR code or enter your temporary ID to check out.</p>
            </div>
          </div>
        </div>
        <div class="input-group mx-4 mb-3" style="width: 90%;">
          <input type="text" id="chatInput" class="form-control form-control-lg" placeholder="Ask me anything...">
          <button class="btn btn-primary" id="sendChat">
            <i class="fas fa-paper-plane"></i>
          </button>
        </div>
        <div class="mt-2 mx-4 mb-4">
          <p class="text-muted fw-medium small" style="word-wrap: break-word; overflow-wrap: break-word;">Ashley can help you with:</p>
          <ul class="text-muted small" style="word-wrap: break-word; overflow-wrap: break-word; padding-right: 10px;">
            <li>Checkout procedures</li>
            <li>Finding your way around</li>
            <li>General inquiries</li>
            <li>Registration for your next visit</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Checkout form on the right -->
    <div class="col-md-8">
      <div class="card h-100 shadow-sm">
        <div class="card-header bg-danger text-white p-4">
          <h2 class="mb-0">Visitor Checkout</h2>
        </div>
        <div class="card-body p-4">
          <form method="post" action="/checkout">
            <div class="mb-4">
              <label class="form-label fw-medium">Scan QR Code or Enter Temp ID:</label>
              <input class="form-control form-control-lg" type="text" name="temp_id" id="temp_id" required>
            </div>
            <div class="d-grid gap-2">
              <button class="btn btn-danger btn-lg btn-raised" type="submit">
                <i class="fas fa-sign-out-alt me-2"></i>Checkout
              </button>
              <button class="btn btn-secondary btn-lg btn-raised" type="button" onclick="startScan()">
                <i class="fas fa-qrcode me-2"></i>Scan QR Code
              </button>
            </div>
          </form>
          <div id="qr-reader" class="mt-4" style="width:100%"></div>
          {% with messages = get_flashed_messages() %}
            {% if messages %}
              <div class="alert alert-info mt-3">
                <ul class="mb-0">{% for msg in messages %}<li>{{ msg }}</li>{% endfor %}</ul>
              </div>
            {% endif %}
          {% endwith %}
          <div class="mt-4 text-center">
            <a class="btn btn-outline-primary btn-raised" href="/">
              <i class="fas fa-arrow-left me-2"></i>Back to Registration
            </a>
          </div>
        </div>
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
