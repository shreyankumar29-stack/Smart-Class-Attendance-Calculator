from .login_api import register_login_api
from .dashboard_api import register_dashboard_api
from .subjects_api import register_subjects_api
from .attendance_api import register_attendance_api


def register_api_routes(app):

    register_login_api(app)
    register_dashboard_api(app)
    register_subjects_api(app)
    register_attendance_api(app)