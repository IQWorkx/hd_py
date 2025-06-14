from flask import render_template_string

BOOTSTRAP_CDN = '''
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-material-design/4.0.2/bootstrap-material-design.min.css">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
'''

LIGHT_THEME_CSS = '''
<style>
body { background: #f8f9fa; color: #222; font-family: Arial, sans-serif; }
h2 { color: #007bff; }
h3 { color: #0056b3; }
h4 { color: #0056b3; }
a { color: #007bff; text-decoration: none; }
a:hover { text-decoration: underline; color: #0056b3; }
ul { color: #d9534f; }

/* Optimized form elements */
.form-label { color: #333; font-weight: 500; font-size: 0.95rem; }
.text-muted { color: #555 !important; }
.small.text-muted { color: #666 !important; }
.form-control { font-size: 0.95rem; }
.form-control-lg { font-size: 1.05rem; }

/* Optimized chat messages */
.chat-message-user { background-color: #e3f2fd; border-color: #90caf9; font-size: 0.95rem; word-wrap: break-word; overflow-wrap: break-word; }
.chat-message-bot { background-color: #f1f8e9; border-color: #aed581; font-size: 0.95rem; word-wrap: break-word; overflow-wrap: break-word; }
/* Ensure all chat messages have proper text wrapping and font size */
[class*="chat-message"] { font-size: 0.95rem !important; word-wrap: break-word !important; overflow-wrap: break-word !important; }
[class*="chat-message"] p { font-size: 0.95rem !important; margin-bottom: 0 !important; }

/* Optimized card elements */
.card-title { color: #0056b3; }
.card-header { font-weight: 500; }
.card-header.bg-primary { background-color: #f0f7ff !important; color: #0056b3 !important; border-bottom: 2px solid #007bff; }
.card-header.bg-success { background-color: #f0fff5 !important; color: #28a745 !important; border-bottom: 2px solid #28a745; }
.card-header.bg-danger { background-color: #fff5f5 !important; color: #dc3545 !important; border-bottom: 2px solid #dc3545; }
.fw-bold { color: #333; }

/* Optimized buttons */
.btn { font-size: 0.95rem; }
.btn-lg { font-size: 1.05rem; }
.btn-primary { background-color: #1976d2; border-color: #1976d2; }
.btn-primary:hover { background-color: #1565c0; border-color: #1565c0; }
.btn-danger { background-color: #e53935; border-color: #e53935; }
.btn-danger:hover { background-color: #d32f2f; border-color: #d32f2f; }
.btn-outline-primary { color: #1976d2; border-color: #1976d2; }
.btn-outline-primary:hover { background-color: #1976d2; border-color: #1976d2; }

/* Optimized alerts */
.alert-info { background-color: #e3f2fd; border-color: #90caf9; color: #0d47a1; }
</style>
'''

HEADER = '''
<nav class="navbar navbar-expand-lg navbar-light bg-light mb-4">
  <div class="container-fluid">
    <a class="navbar-brand" href="/admin/dashboard">
      <i class="fas fa-robot me-2"></i>AI-Powered Visitor Portal
    </a>
    <div class="d-flex">
      <a class="nav-link" href="/admin/export">Export to Excel</a>
      <a class="nav-link" href="/admin/logout">Logout</a>
    </div>
  </div>
</nav>
'''

FOOTER = '''
<footer class="footer mt-auto py-3 bg-light text-center">
  <div class="container">
    <span class="text-muted">&copy; 2025 AI-Powered Visitor Management System</span>
    <div class="mt-1">
      <small class="text-muted">Powered by Advanced AI Technology</small>
    </div>
  </div>
</footer>
'''

def themed(html, admin=False):
    base = BOOTSTRAP_CDN + LIGHT_THEME_CSS
    if admin:
        return base + HEADER + html + FOOTER
    return base + html
