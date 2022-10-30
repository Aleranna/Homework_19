from flask import request
from flask_restx import Resource, Namespace
from utils import auth_required, admin_required

from dao.model.director import DirectorSchema
from implemented import director_service

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        rs = director_service.get_all()
        res = DirectorSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        data = request.json
        res = director_service.create(data)
        return "info added", 201, {"location": f"/directors/{res.id}"}


@director_ns.route('/<int:rid>')
class DirectorView(Resource):
    @auth_required
    def get(self, rid):
        r = director_service.get_one(rid)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self):
        data = request.json
        res = director_service.update(data)
        return res, 201

    @admin_required
    def delete(self, did):
        director_service.delete(did)
        return 'info deleted', 204


