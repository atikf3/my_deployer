import os
from flask import request, current_app as app
from flask import jsonify, make_response
from flask_restplus import Api, Resource, fields, reqparse
import docker


__author__ = 'talamo_a'


api = Api(app,
          version='1.0',
          title='my_deployer - checker',
          description='ETNA Project my_deployer checker\n\n'
                'Copyright (c) 2020 talamo_a@etna-alternance.net\n'
                'Please see LICENSE file for more information.',)
client = docker.DockerClient(base_url=os.environ.get('DOCKER_URL'))

containers_parser = api.parser()
containers_parser.add_argument('all', default='true', required=False,
                               choices=('true', 'false'))


@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error=404, text=str(e)), 404


@api.route('/containers', doc={
    "description": "Fetch containers",
    "deprecated": False})
class _containers(Resource):
    @api.doc(responses={500: 'Server error', 400: 'Bad request',
                        404: 'Not found', 200: 'OK'}, parser=containers_parser)
    def get(self):
        """ Returns all containers (even stopped ones) if the all query """
        """ parameter is set to true. Returns a list of containers  """
        """ currently running on the host otherwise. """
        containers = client.containers.list(all=(
            request.args.get('all') == 'true'))
        res = []
        for container in containers:
            res.append(container.attrs)
        return jsonify(res)


@api.route('/containers/<int:id>', doc={
    "description": "Fetch containers",
    "deprecated": False})
class _containers(Resource):
    @api.doc(responses={500: 'Server error', 400: 'Bad request',
                        404: 'Not found', 200: 'OK'})
    def get(self, id):
        """ Returns all containers (even stopped ones) if the all query """
        """ parameter is set to true. Returns a list of containers  """
        """ currently running on the host otherwise. """
        try:
            container = client.containers.get(container_id=str(id))
        except docker.errors.NotFound:
            return {'error': 404, 'reason': 'Container not found.'}, 404
        except docker.errors.APIError:
            return {'error': 404, 'reason': 'Docker server error.'}, 500
        return jsonify(container.attrs)
