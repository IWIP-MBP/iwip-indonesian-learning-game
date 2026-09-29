from flask import Blueprint

language_game_bp = Blueprint('language_game', __name__)

# Import blueprint routes to register them
from .blueprints.auth import auth_bp
from .blueprints.course import course_bp
from .blueprints.game import game_bp
from .blueprints.ranking import ranking_bp
from .blueprints.report import report_bp
from .blueprints.admin import admin_bp
from .blueprints.special_study import special_study_bp

# Register sub-blueprints
language_game_bp.register_blueprint(auth_bp)
language_game_bp.register_blueprint(course_bp)
language_game_bp.register_blueprint(game_bp)
language_game_bp.register_blueprint(ranking_bp)
language_game_bp.register_blueprint(report_bp)
language_game_bp.register_blueprint(admin_bp)
language_game_bp.register_blueprint(special_study_bp)
