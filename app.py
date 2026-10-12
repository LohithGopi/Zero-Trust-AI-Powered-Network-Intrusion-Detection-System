import os
from flask import Flask, render_template, redirect, url_for, g, jsonify, request, send_from_directory
from config import Config
from database.init_db import init_db, db, DatasetHistory, ModelHistory, AuditLog
from security.jwt_auth import get_token_from_request, decode_token
from security.zero_trust import jwt_required
from api.auth_routes import auth_bp
from api.dataset_routes import dataset_bp
from api.model_routes import model_bp
from api.live_detection_routes import live_detection_bp
from utils.logger import logger, log_audit_event

def create_app():
    """Application Factory for AI Zero Trust NIDS Flask Web Application."""
    app = Flask(__name__, static_folder='frontend/dist', static_url_path='')
    app.config.from_object(Config)

    # Initialize app directories and database
    Config.init_app(app)
    init_db(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dataset_bp)
    app.register_blueprint(model_bp)
    app.register_blueprint(live_detection_bp)

    @app.before_request
    def load_user_context():
        """Zero Trust Context Middleware: Extract token & user details if present."""
        g.user = None
        token = get_token_from_request()
        if token:
            payload = decode_token(token)
            if "error" not in payload:
                g.user = payload

    @app.after_request
    def add_no_cache_headers(response):
        """Ensure browser loads latest React build bundle without stale caching."""
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

    @app.route("/")
    def index():
        """Serve application directly on app.py (http://127.0.0.1:5000)."""
        dist_index = os.path.join(app.root_path, 'frontend', 'dist', 'index.html')
        if os.path.exists(dist_index):
            return send_from_directory('frontend/dist', 'index.html')
        
        # Fallback to Jinja dashboard
        datasets = DatasetHistory.query.all()
        selected_ds = DatasetHistory.query.filter_by(is_selected=True).first()
        if not selected_ds and datasets:
            selected_ds = datasets[0]

        latest_model = ModelHistory.query.order_by(ModelHistory.trained_at.desc()).first()
        audit_logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(15).all()

        stats = {
            "total_datasets": len(datasets),
            "selected_dataset": selected_ds.filename if selected_ds else None,
            "selected_rows": selected_ds.row_count if selected_ds else 0,
            "selected_cols": selected_ds.col_count if selected_ds else 0,
            "model_trained": latest_model is not None,
            "last_trained": latest_model.trained_at.strftime("%Y-%m-%d %H:%M") if latest_model else "Never",
            "latest_acc": f"{round(latest_model.accuracy * 100, 2)}%" if latest_model else "N/A"
        }

        return render_template(
            "dashboard.html",
            stats=stats,
            audit_logs=[log.to_dict() for log in audit_logs],
            user=g.user
        )

    # Serve static JS/CSS assets directly from frontend/dist/assets
    @app.route('/assets/<path:path>')
    def serve_assets(path):
        return send_from_directory('frontend/dist/assets', path)

    @app.route('/jnnce_logo.png')
    def serve_logo():
        return send_from_directory('frontend/public', 'jnnce_logo.png')

    @app.route("/trojan")
    @app.route("/academic")
    def spa_landing_routes():
        dist_index = os.path.join(app.root_path, 'frontend', 'dist', 'index.html')
        if os.path.exists(dist_index):
            return send_from_directory('frontend/dist', 'index.html')
        return redirect(url_for("index"))

    @app.route('/<path:path>')
    def serve_static_or_spa(path):
        dist_file = os.path.join(app.root_path, 'frontend', 'dist', path)
        if os.path.exists(dist_file):
            return send_from_directory('frontend/dist', path)
        public_file = os.path.join(app.root_path, 'frontend', 'public', path)
        if os.path.exists(public_file):
            return send_from_directory('frontend/public', path)
        if not path.startswith('api/'):
            dist_index = os.path.join(app.root_path, 'frontend', 'dist', 'index.html')
            if os.path.exists(dist_index):
                return send_from_directory('frontend/dist', 'index.html')
        return jsonify({"error": "Resource Not Found"}), 404

    # Error Handlers
    @app.errorhandler(400)
    def bad_request(e):
        if request.path.startswith("/api/"):
            return jsonify({"error": "Bad Request", "message": str(e)}), 400
        return render_template("base.html", error="Bad Request"), 400

    @app.errorhandler(401)
    def unauthorized(e):
        if request.path.startswith("/api/"):
            return jsonify({"error": "Unauthorized", "message": "JWT Token Required"}), 401
        return redirect(url_for("auth.login_page"))

    @app.errorhandler(403)
    def forbidden(e):
        if request.path.startswith("/api/"):
            return jsonify({"error": "Forbidden", "message": "Access Denied by Zero Trust RBAC Policy"}), 403
        return jsonify({"error": "Access Denied. Insufficient permissions."}), 403

    @app.errorhandler(404)
    def page_not_found(e):
        if request.path.startswith("/api/"):
            return jsonify({"error": "Resource Not Found"}), 404
        dist_index = os.path.join(app.root_path, 'frontend', 'dist', 'index.html')
        if os.path.exists(dist_index):
            return send_from_directory('frontend/dist', 'index.html')
        return render_template("base.html", error="Page Not Found"), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        if request.path.startswith("/api/"):
            return jsonify({"error": "Method Not Allowed", "message": str(e)}), 405
        return render_template("base.html", error="Method Not Allowed"), 405

    @app.errorhandler(500)
    def internal_server_error(e):
        logger.error(f"Unhandled Server Exception: {str(e)}")
        if request.path.startswith("/api/"):
            return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
        return render_template("base.html", error="Internal Server Error"), 500

    return app

app = create_app()

if __name__ == "__main__":
    logger.info("Starting Zero Trust AI-Powered NIDS Flask Web Server on http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)
