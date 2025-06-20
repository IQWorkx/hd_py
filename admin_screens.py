from flask import render_template_string, render_template, request
from theme import themed

# Common CSS for admin pages
ADMIN_CSS = '''
<style>
  body {
    background: #f8f9fa;
    color: #222;
    font-family: 'Roboto', Arial, sans-serif;
    min-height: 100vh;
  }
  .header-bar {
    width: 100vw;
    background: #fff;
    color: #009688;
    border-bottom: 1px solid #e0e0e0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.5rem 2rem 0.5rem 0.5rem;
    position: fixed;
    top: 0;
    left: 0;
    z-index: 1100;
    height: 64px;
    box-shadow: 0 2px 8px rgba(0,150,136,0.08);
  }
  .header-logo {
    display: flex;
    align-items: center;
  }
  .header-logo img {
    height: 40px;
    margin-right: 0.75rem;
  }
  .side-nav {
    position: fixed;
    top: 64px;
    left: 0;
    height: calc(100vh - 64px);
    width: 220px;
    background: #fff;
    color: #222;
    z-index: 1000;
    padding-top: 2rem;
    box-shadow: 2px 0 12px rgba(0,150,136,0.08);
    border-right: 1px solid #e0e0e0;
    transition: width 0.3s;
  }
  .side-nav.collapsed {
    width: 60px;
    padding-top: 1rem;
  }
  .side-nav .nav-link {
    color: #222;
    font-weight: 500;
    padding: 1rem 1.5rem;
    border-radius: 0 2rem 2rem 0;
    margin-bottom: 0.5rem;
    transition: background 0.2s, color 0.2s;
    white-space: nowrap;
  }
  .side-nav.collapsed .nav-link span {
    display: none;
  }
  .side-nav .nav-link i {
    margin-right: 0.5rem;
  }
  .side-nav.collapsed .nav-link {
    text-align: center;
    padding: 1rem 0.5rem;
  }
  .side-nav .nav-link.active, .side-nav .nav-link:hover {
    background: #e0f2f1;
    color: #009688;
  }
  .main-content {
    margin-left: 220px;
    margin-top: 80px;
    transition: margin-left 0.3s;
  }
  .side-nav.collapsed ~ .main-content {
    margin-left: 60px;
  }
  @media (max-width: 991px) {
    .main-content { margin-left: 70px; }
    .side-nav { width: 70px; }
    .side-nav.collapsed { width: 0; }
  }
  @media (max-width: 575px) {
    .main-content { margin-left: 0; margin-top: 100px; }
    .side-nav { width: 0; }
    .side-nav.collapsed { width: 0; }
  }
  .dashboard-header {
    background: #fff;
    color: #009688;
    border-radius: 0.75rem;
    padding: 1.5rem 1rem 1rem 1rem;
    margin-bottom: 2rem;
    box-shadow: 0 4px 24px rgba(0,150,136,0.10);
    border: 1px solid #e0e0e0;
  }
  .dashboard-header h2 {
    color: #009688;
    margin-bottom: 0;
    font-weight: 500;
    letter-spacing: 0.5px;
  }
  .card, .table {
    background: #fff;
    border-radius: 1rem;
    border: 1px solid #e0e0e0;
    box-shadow: 0 2px 8px rgba(0,150,136,0.04);
  }
  .visitor-card .card-title {
    color: #009688;
  }
  .visitor-card .list-group-item strong {
    color: #009688;
  }
  .btn-outline-primary.btn-sm, .btn-primary.btn-sm {
    border-color: #009688;
    color: #009688;
    background: #fff;
  }
  .btn-outline-primary.btn-sm:hover, .btn-primary.btn-sm:hover {
    background: #009688;
    color: #fff;
  }
  /* DataTables button styling */
  .dt-buttons .btn {
    border-color: #009688;
    background-color: #009688;
    color: #fff;
  }
  .dt-buttons .btn:hover {
    background-color: #00796b;
    border-color: #00796b;
    color: #fff;
  }
  .dt-buttons .btn i {
    color: #fff;
  }
  /* Custom export button styling */
  #exportCurrentVisitors, #exportVisitorHistory {
    background-color: #009688;
    border-color: #009688;
    color: #fff;
  }
  #exportCurrentVisitors:hover, #exportVisitorHistory:hover {
    background-color: #00796b;
    border-color: #00796b;
  }
  .badge.bg-primary {
    background-color: #009688 !important;
  }
  .table thead.table-light th {
    background: #e0f2f1;
    color: #009688;
    font-weight: 500;
  }
  .dropdown-menu-end {
    right: 0;
    left: auto;
  }
</style>
'''

# Common JavaScript for admin pages
ADMIN_JS = '''
<script>
  $(function() {
    // Sidebar toggle
    $('#sidebarToggle').on('click', function() {
      $('.side-nav').toggleClass('collapsed');
      if ($('.side-nav').hasClass('collapsed')) {
        $('.main-content').css('margin-left', '60px');
      } else {
        $('.main-content').css('margin-left', '220px');
      }
    });
    // MDB Dropdown fallback
    if (typeof mdb !== 'undefined' && mdb.Dropdown) {
      var dropdownElementList = [].slice.call(document.querySelectorAll('.dropdown-toggle'));
      dropdownElementList.map(function (dropdownToggleEl) {
        return new mdb.Dropdown(dropdownToggleEl);
      });
    }
  });
</script>
'''

def render_admin_header(page_id="Dashboard", page_title=None):
    # Use a more descriptive page title if provided
    title = page_title if page_title else page_id.replace("Dashboard", "Dashboard").replace("Current", "Current Visitors").replace("History", "Visitor History")

    # Determine which nav link should be active based on page_id
    dashboard_active = "active" if page_id == "Dashboard" else ""
    current_active = "active" if page_id == "Current" else ""
    history_active = "active" if page_id == "History" else ""

    return f'''
    <!-- Material Design Bootstrap CSS -->
    <link rel="stylesheet" href="{{{{ url_for('static', filename='css/mdb.min.css') }}}}" />
    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet" />
    <!-- jQuery -->
    <script src="{{{{ url_for('static', filename='js/jquery-3.7.0.min.js') }}}}"></script>
    <!-- MDB -->
    <script src="{{{{ url_for('static', filename='js/mdb.min.js') }}}}"></script>

    {ADMIN_CSS}

    <div class="header-bar">
      <div class="header-logo">
        <button id="sidebarToggle" class="btn btn-link text-teal me-2" style="font-size: 1.5rem;">
          <i class="fas fa-bars"></i>
        </button>
        <!-- <img src="https://mdbcdn.b-cdn.net/img/logo/mdb-transaprent-noshadows.png" alt="Logo">  -->
        <span class="fs-4 fw-bold">Admin Panel</span>
      </div>
      <div class="d-flex align-items-center">
        <div class="d-flex align-items-center me-3">
          <i class="fas fa-user-circle fa-lg me-2"></i>
          <span class="text-dark">{{ session.get('admin_username', 'Admin User') }}</span>
        </div>
        <a href="/admin/logout" class="btn btn-outline-danger btn-sm">
          <i class="fas fa-sign-out-alt me-1"></i> Logout
        </a>
      </div>
    </div>

    <!-- Side Navigation -->
    <div class="side-nav">
      <a class="nav-link {dashboard_active}" href="/admin/dashboard">
        <i class="fas fa-tachometer-alt"></i> <span>Dashboard</span>
      </a>
      <a class="nav-link {current_active}" href="/admin/current-visitors">
        <i class="fas fa-users"></i> <span>Current Visitors</span>
      </a>
      <a class="nav-link {history_active}" href="/admin/historical-visitors">
        <i class="fas fa-history"></i> <span>Visitor History</span>
      </a>
    </div>

    <div class="main-content container d-flex flex-column align-items-center mt-4">
      <div class="dashboard-header w-100 text-center">
        <h2 class="mb-0">{title}</h2>
      </div>

    {ADMIN_JS}
    '''

def render_admin_login_form():
    return render_template('login.html')

def render_admin_stats_dashboard(total_visitors, today_visitors, current_visitors, historical_visitors, chart_data):
    return render_template('dashboard.html',
        active_page='dashboard',
        total_visitors=total_visitors,
        today_visitors=today_visitors,
        current_visitors=current_visitors,
        historical_visitors=historical_visitors,
        chart_data=chart_data)

def render_current_visitors(current_visitors):
    return render_template('current_visitors.html',
        active_page='current',
        current_visitors=current_visitors)

def render_historical_visitors(historical_visitors):
    return render_template('historical_visitors.html',
        active_page='history',
        historical_visitors=historical_visitors)

def render_admin_dashboard(current_visitors, historical_visitors):
    # For backward compatibility: show both tables on one page (legacy usage)
    return render_template('combined_dashboard.html',
        active_page='dashboard',
        current_visitors=current_visitors,
        historical_visitors=historical_visitors)

def render_theme_config_form(current_logo, current_theme_color):
    return '''
    <form method="post" enctype="multipart/form-data" class="mb-4" style="max-width: 400px;">
        <div class="mb-3">
            <label for="siteLogo" class="form-label">Site Logo</label>
            <input type="file" class="form-control" id="siteLogo" name="siteLogo" accept="image/*">
            <div class="form-text">Current: <img src="/static/{}" alt="Logo" style="height:32px;vertical-align:middle;"></div>
        </div>
        <div class="mb-3">
            <label for="themeColor" class="form-label">Theme Color</label>
            <input type="color" class="form-control form-control-color" id="themeColor" name="themeColor" value="{}" title="Choose your color">
        </div>
        <button type="submit" class="btn btn-primary">Update Theme</button>
    </form>
    '''.format(current_logo, current_theme_color)
