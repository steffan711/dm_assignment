from flask import Blueprint, jsonify, request
from data_manager import DataManager


def create_api_blueprint():
    """
    Create and configure a Flask Blueprint for the API.

    Returns:
        Flask Blueprint: Configured Flask Blueprint for handling API requests.
    """
    api_blueprint = Blueprint('api', __name__)

    @api_blueprint.route('/statistics', methods=['GET'])
    def statistics():
        """
        Endpoint for fetching statistics of a given repository.
        Expects 'repository_name' as a query parameter.

        Returns:
            JSON response containing the statistics of the requested repository.
        """
        repository = request.args.get('repository_name')
        if not repository:
            return jsonify({"error": "Repository name is required"}), 400

        data_manager = DataManager()
        data = data_manager.get_statistics(repository)
        return jsonify(data)

    return api_blueprint
