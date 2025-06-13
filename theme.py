from flask import render_template_string

BOOTSTRAP_CDN = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">'

LIGHT_THEME_CSS = '''
<style>
body { background: #f8f9fa; color: #222; font-family: Arial, sans-serif; }
h2 { color: #007bff; }
a { color: #007bff; text-decoration: none; }
a:hover { text-decoration: underline; }
ul { color: #d9534f; }
</style>
'''

HEADER = '''
<nav class="navbar navbar-expand-lg navbar-light bg-light mb-4">
  <div class="container-fluid">
    <a class="navbar-brand" href="/admin/dashboard">Helpdesk Admin</a>
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
    <span class="text-muted">&copy; 2025 Company Helpdesk</span>
  </div>
</footer>
'''

def themed(html, admin=False):
    base = BOOTSTRAP_CDN + LIGHT_THEME_CSS
    if admin:
        return base + HEADER + html + FOOTER
    return base + html
