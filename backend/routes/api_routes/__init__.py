from .login_api import register_login_api
from .dashboard_api import register_dashboard_api
from .subjects_api import register_subjects_api
from .attendance_api import register_attendance_api
from .analytics_api import register_analytics_api
from .profile_api import register_profile_api
from .register_api import register_register_api
def register_api_routes(app):

    register_login_api(app)
    register_dashboard_api(app)
    register_subjects_api(app)
    register_attendance_api(app)
    register_analytics_api(app)
    register_register_api(app)
    register_profile_api(app)