from flask import Blueprint, render_template, make_response, jsonify

errors_Bp = Blueprint('errors', __name__)


@errors_Bp.app_errorhandler(404)
def not_found(error):
    #return render_template('errors/404.html'), 404
    return make_response(jsonify({'error': 'Not found'}), 404)

@errors_Bp.app_errorhandler(403)
def forbidden(error):
    #return render_template('errors/403.html'), 403
    return make_response(jsonify({'error': 'forbidden'}), 403)


@errors_Bp.app_errorhandler(500)
def internal_server_error(error):
    # return render_template('errors/500.html'), 500
    return make_response(jsonify({'error': 'internal_server_error'}), 500)
