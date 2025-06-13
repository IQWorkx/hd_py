from flask import render_template_string, request
from theme import themed

def render_admin_header(page_id="Dashboard", page_title=None):
    dropdown_id = f"userDropdown"
    # Use a more descriptive page title if provided
    title = page_title if page_title else page_id.replace("Dashboard", "Dashboard").replace("Current", "Current Visitors").replace("History", "Visitor History")
    return f'''
    <div class="header-bar">
      <div class="header-logo">
        <button id="sidebarToggle" class="btn btn-link text-teal me-2" style="font-size: 1.5rem;">
          <i class="fas fa-bars"></i>
        </button>
        <!-- <img src="https://mdbcdn.b-cdn.net/img/logo/mdb-transaprent-noshadows.png" alt="Logo">  -->
        <span class="fs-4 fw-bold">Admin Panel</span>
      </div>
      <div class="dropdown">
        <button class="btn btn-link text-teal dropdown-toggle" type="button" id="{dropdown_id}" data-mdb-toggle="dropdown" aria-expanded="false">
          <i class="fas fa-user-circle fa-lg me-2"></i> Admin
        </button>
        <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="{dropdown_id}">
          <li><span class="dropdown-item-text"><i class="fas fa-user me-2"></i>Admin User</span></li>
          <li><hr class="dropdown-divider"></li>
          <li><a class="dropdown-item text-danger" href="/admin/logout"><i class="fas fa-sign-out-alt me-2"></i>Logout</a></li>
        </ul>
      </div>
    </div>
    <div class="main-content container d-flex flex-column align-items-center mt-4">
      <div class="dashboard-header w-100 text-center">
        <h2 class="mb-0">{title}</h2>
      </div>
    '''

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

def render_admin_stats_dashboard(total_visitors, today_visitors, current_visitors, historical_visitors, chart_data):
    dashboard_html = '''
    <!-- Material Design Bootstrap CSS -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/7.2.0/mdb.min.css" />
    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet" />
    <!-- DataTables CSS -->
    <link rel="stylesheet" href="https://cdn.datatables.net/1.13.7/css/dataTables.bootstrap5.min.css" />
    <link rel="stylesheet" href="https://cdn.datatables.net/buttons/2.4.2/css/buttons.bootstrap5.min.css" />
    <!-- jQuery -->
    <script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
    <!-- Popper.js for MDB dropdowns -->
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js"></script>
    <!-- MDB -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/7.2.0/mdb.min.js"></script>
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
    <!-- DataTables JS -->
    <script src="https://cdn.datatables.net/1.13.7/js/jquery.dataTables.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.7/js/dataTables.bootstrap5.min.js"></script>
    <!-- DataTables Buttons for Excel export -->
    <script src="https://cdn.datatables.net/buttons/2.4.2/js/dataTables.buttons.min.js"></script>
    <script src="https://cdn.datatables.net/buttons/2.4.2/js/buttons.bootstrap5.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
    <script src="https://cdn.datatables.net/buttons/2.4.2/js/buttons.html5.min.js"></script>
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
    ''' + render_admin_header("Dashboard", "Dashboard Overview") + '''
    <div class="side-nav d-flex flex-column">
      <a class="nav-link{% if request.path == '/admin/dashboard' %} active{% endif %}" href="/admin/dashboard"><i class="fas fa-tachometer-alt me-2"></i> <span>Dashboard</span></a>
      <a class="nav-link{% if request.path == '/admin/current-visitors' %} active{% endif %}" href="/admin/current-visitors"><i class="fas fa-users me-2"></i> <span>Visitor</span></a>
      <a class="nav-link{% if request.path == '/admin/historical-visitors' %} active{% endif %}" href="/admin/historical-visitors"><i class="fas fa-history me-2"></i> <span>Historical Visitor</span></a>
    </div>
    <div class="container mt-4">
      <div class="row mb-4">
        <div class="col-md-3 col-6 mb-3">
          <div class="card text-center shadow-sm">
            <div class="card-body">
              <h6 class="card-title">Total Visitors</h6>
              <div class="display-6 fw-bold">{{ total_visitors }}</div>
            </div>
          </div>
        </div>
        <div class="col-md-3 col-6 mb-3">
          <div class="card text-center shadow-sm">
            <div class="card-body">
              <h6 class="card-title">Today's Visitors</h6>
              <div class="display-6 fw-bold">{{ today_visitors }}</div>
            </div>
          </div>
        </div>
        <div class="col-md-3 col-6 mb-3">
          <div class="card text-center shadow-sm">
            <div class="card-body">
              <h6 class="card-title">Current Visitors</h6>
              <div class="display-6 fw-bold">{{ current_visitors }}</div>
            </div>
          </div>
        </div>
        <div class="col-md-3 col-6 mb-3">
          <div class="card text-center shadow-sm">
            <div class="card-body">
              <h6 class="card-title">Historical Visitors</h6>
              <div class="display-6 fw-bold">{{ historical_visitors }}</div>
            </div>
          </div>
        </div>
      </div>
      <div class="card mb-4">
        <div class="card-body">
          <h5 class="card-title">Visitors Per Day (Last 7 Days)</h5>
          <canvas id="visitorsChart" style="max-width:100%;height:320px;"></canvas>
        </div>
      </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
      const chartData = {{ chart_data|tojson }};
      const ctx = document.getElementById(\"visitorsChart\").getContext(\"2d\");
      new Chart(ctx, {
        \"type\": \"bar\",
        \"data\": {
          \"labels\": chartData.map(d => d.day),
          \"datasets\": [{
            \"label\": \"Visitors\",
            \"data\": chartData.map(d => d.count),
            \"backgroundColor\": \"#673ab7\"
          }]
        },
        \"options\": {
          \"responsive\": true,
          \"plugins\": { \"legend\": { \"display\": false } }
        }
      });
    </script>
    '''
    return render_template_string(themed(dashboard_html, admin=True),
        total_visitors=total_visitors,
        today_visitors=today_visitors,
        current_visitors=current_visitors,
        historical_visitors=historical_visitors,
        chart_data=chart_data)

def render_current_visitors(current_visitors):
    current_visitors_html = '''
    <!-- Material Design Bootstrap CSS -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/7.2.0/mdb.min.css" />
    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet" />
    <!-- DataTables CSS -->
    <link rel="stylesheet" href="https://cdn.datatables.net/1.13.7/css/dataTables.bootstrap5.min.css" />
    <link rel="stylesheet" href="https://cdn.datatables.net/buttons/2.4.2/css/buttons.bootstrap5.min.css" />
    <!-- jQuery -->
    <script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
    <!-- Popper.js for MDB dropdowns -->
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js"></script>
    <!-- MDB -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/7.2.0/mdb.min.js"></script>
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
    <!-- DataTables JS -->
    <script src="https://cdn.datatables.net/1.13.7/js/jquery.dataTables.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.7/js/dataTables.bootstrap5.min.js"></script>
    <!-- DataTables Buttons for Excel export -->
    <script src="https://cdn.datatables.net/buttons/2.4.2/js/dataTables.buttons.min.js"></script>
    <script src="https://cdn.datatables.net/buttons/2.4.2/js/buttons.bootstrap5.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
    <script src="https://cdn.datatables.net/buttons/2.4.2/js/buttons.html5.min.js"></script>
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
    ''' + render_admin_header("Current", "Current Visitors List") + '''
    <div class="side-nav d-flex flex-column">
      <a class="nav-link{% if request.path == '/admin/dashboard' %} active{% endif %}" href="/admin/dashboard"><i class="fas fa-tachometer-alt me-2"></i> <span>Dashboard</span></a>
      <a class="nav-link{% if request.path == '/admin/current-visitors' %} active{% endif %}" href="/admin/current-visitors"><i class="fas fa-users me-2"></i> <span>Visitor</span></a>
      <a class="nav-link{% if request.path == '/admin/historical-visitors' %} active{% endif %}" href="/admin/historical-visitors"><i class="fas fa-history me-2"></i> <span>Historical Visitor</span></a>
    </div>
    <div class="container mt-4">
      <div class="card">
        <div class="card-body">
          <table id="currentVisitorsTable" class="table table-bordered table-striped">
            <thead class="table-light">
            <tr>
              <th>Sl No</th>
              <th>Name</th>
              <th>Company</th>
              <th>Phone</th>
              <th>Email</th>
              <th>Purpose</th>
              <th>Whom to Meet</th>
              <th>Check-In</th>
              <th>Actions</th>
            </tr>
            </thead>
            <tbody>
            {% for v in current_visitors %}
              <tr>
                <td>{{ loop.index }}</td>
                <td>{{ v.name }}</td>
                <td>{{ v.company }}</td>
                <td>{{ v.phone }}</td>
                <td>{{ v.email }}</td>
                <td>{{ v.purpose }}</td>
                <td>{{ v.whom_to_meet }}</td>
                <td>{{ v.checkin_time|datetime('medium') }}</td>
                <td><a class="btn btn-sm btn-warning" href="/admin/logout_visitor/{{ v.id }}"><i class="fas fa-sign-out-alt me-2"></i>Clock Out</a></td>
              </tr>
            {% endfor %}
            </tbody>
          </table>
        </div>
      </div>
    </div>
    <script>
      $(document).ready(function() {
        var table = $("#currentVisitorsTable").DataTable({
          "dom": "Bfrtip",
          "buttons": [
            {
              "extend": "excel",
              "text": "<i class=\\"fas fa-file-excel me-2\\"></i>Download",
              "className": "btn btn-sm btn-primary dt-custom-btn",
              "filename": "current_visitors"
            }
          ]
        });
        $("#exportCurrentVisitors").on("click", function() {
          table.button(".buttons-excel").trigger();
        });
      });
    </script>
    '''
    return render_template_string(themed(current_visitors_html, admin=True), current_visitors=current_visitors)

def render_historical_visitors(historical_visitors):
    historical_visitors_html = '''
    <!-- Material Design Bootstrap CSS -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/7.2.0/mdb.min.css" />
    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet" />
    <!-- DataTables CSS -->
    <link rel="stylesheet" href="https://cdn.datatables.net/1.13.7/css/dataTables.bootstrap5.min.css" />
    <link rel="stylesheet" href="https://cdn.datatables.net/buttons/2.4.2/css/buttons.bootstrap5.min.css" />
    <!-- jQuery -->
    <script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
    <!-- Popper.js for MDB dropdowns -->
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js"></script>
    <!-- MDB -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/7.2.0/mdb.min.js"></script>
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
    <!-- DataTables JS -->
    <script src="https://cdn.datatables.net/1.13.7/js/jquery.dataTables.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.7/js/dataTables.bootstrap5.min.js"></script>
    <!-- DataTables Buttons for Excel export -->
    <script src="https://cdn.datatables.net/buttons/2.4.2/js/dataTables.buttons.min.js"></script>
    <script src="https://cdn.datatables.net/buttons/2.4.2/js/buttons.bootstrap5.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
    <script src="https://cdn.datatables.net/buttons/2.4.2/js/buttons.html5.min.js"></script>
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
    ''' + render_admin_header("History", "Visitor History Records") + '''
    <div class="side-nav d-flex flex-column">
      <a class="nav-link{% if request.path == '/admin/dashboard' %} active{% endif %}" href="/admin/dashboard"><i class="fas fa-tachometer-alt me-2"></i> <span>Dashboard</span></a>
      <a class="nav-link{% if request.path == '/admin/current-visitors' %} active{% endif %}" href="/admin/current-visitors"><i class="fas fa-users me-2"></i> <span>Visitor</span></a>
      <a class="nav-link{% if request.path == '/admin/historical-visitors' %} active{% endif %}" href="/admin/historical-visitors"><i class="fas fa-history me-2"></i> <span>Historical Visitor</span></a>
    </div>
    <div class="container mt-4">
      <div class="mb-3">
        <button id="toggleViewBtn" class="btn btn-outline-primary btn-sm">
          <i class="fas fa-table me-2"></i>Switch to Card View
        </button>
      </div>
      <div class="card">
        <div class="card-body">
          <div id="visitorHistoryTableView">
            <table id="visitorHistoryTable" class="table table-bordered table-striped">
              <thead class="table-light">
              <tr>
                <th>Sl No</th>
                <th>Name</th>
                <th>Company</th>
                <th>Phone</th>
                <th>Email</th>
                <th>Purpose</th>
                <th>Whom to Meet</th>
                <th>Temp ID</th>
                <th>Check-In</th>
                <th>Check-Out</th>
              </tr>
              </thead>
              <tbody>
              {% for v in historical_visitors %}
                <tr>
                  <td>{{ loop.index }}</td>
                  <td>{{ v.name }}</td>
                  <td>{{ v.company }}</td>
                  <td>{{ v.phone }}</td>
                  <td>{{ v.email }}</td>
                  <td>{{ v.purpose }}</td>
                  <td>{{ v.whom_to_meet }}</td>
                  <td>{{ v.temp_id }}</td>
                  <td>{{ v.checkin_time|datetime('medium') }}</td>
                  <td>{{ v.checkout_time|datetime('medium') if v.checkout_time else '' }}</td>
                </tr>
              {% endfor %}
              </tbody>
            </table>
          </div>
          <div id="visitorHistoryCardView" style="display:none;">
            <div class="mb-3">
              <input type="text" id="cardSearchInput" class="form-control" placeholder="Search visitor history...">
            </div>
            <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4" id="cardContainer">
              {% for v in historical_visitors %}
              <div class="col visitor-card">
                <div class="card h-100 shadow-sm">
                  <div class="card-body">
                    <h5 class="card-title">{{ v.name }}</h5>
                    <h6 class="card-subtitle mb-2 text-muted">{{ v.company }}</h6>
                    <ul class="list-group list-group-flush mb-2">
                      <li class="list-group-item"><strong>Email:</strong> {{ v.email }}</li>
                      <li class="list-group-item"><strong>Phone:</strong> {{ v.phone }}</li>
                      <li class="list-group-item"><strong>Purpose:</strong> {{ v.purpose }}</li>
                      <li class="list-group-item"><strong>Whom to Meet:</strong> {{ v.whom_to_meet }}</li>
                      <li class="list-group-item"><strong>Temp ID:</strong> {{ v.temp_id }}</li>
                      <li class="list-group-item"><strong>Status:</strong> {{ v.status }}</li>
                      <li class="list-group-item"><strong>Check-In:</strong> {{ v.checkin_time }}</li>
                      <li class="list-group-item"><strong>Check-Out:</strong> {{ v.checkout_time }}</li>
                    </ul>
                  </div>
                  <div class="card-footer text-end">
                    <span class="badge bg-primary">Visitor</span>
                  </div>
                </div>
              </div>
              {% endfor %}
            </div>
            <nav>
              <ul class="pagination justify-content-center mt-3" id="cardPagination"></ul>
            </nav>
          </div>
        </div>
      </div>
    </div>
    <script>
      $(document).ready(function() {
        var historyTable = $("#visitorHistoryTable").DataTable({
          "paging": true,
          "dom": "Bfrtip",
          "buttons": [
            {
              "extend": "excelHtml5",
              "title": "Visitor History",
              "filename": "historical_visitors",
              "text": "<i class=\\"fas fa-file-excel me-2\\"></i>Download",
              "className": "btn btn-sm btn-primary"
            }
          ]
        });
        // Export buttons
        $("#exportVisitorHistory").on("click", function() {
          historyTable.button(0).trigger();
        });
        // Toggle view
        $("#toggleViewBtn").click(function() {
          if ($("#visitorHistoryTableView").is(":visible")) {
            $("#visitorHistoryTableView").hide();
            $("#visitorHistoryCardView").show();
            $(this).html("<i class=\\"fas fa-table me-2\\"></i>Switch to Table View");
          } else {
            $("#visitorHistoryCardView").hide();
            $("#visitorHistoryTableView").show();
            $(this).html("<i class=\\"fas fa-grip-horizontal me-2\\"></i>Switch to Card View");
          }
        });
      });
    </script>
    '''
    return render_template_string(themed(historical_visitors_html, admin=True), historical_visitors=historical_visitors)

def render_admin_dashboard(current_visitors, historical_visitors):
    # For backward compatibility: show both tables on one page (legacy usage)
    return render_current_visitors(current_visitors) + render_historical_visitors(historical_visitors)
