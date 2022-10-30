from flask import request
from flask_restx import Resource, Namespace
from utils import auth_required, admin_required
from dao.model.genre import GenreSchema
from implemented import genre_service

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    @auth_required
    def get(self):
        rs = genre_service.get_all()
        res = GenreSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        data = request.json
        res = genre_service.create(data)
        return "info added", 201, {"location": f"/genres/{res.id}"}


@genre_ns.route('/<int:rid>')
class GenreView(Resource):
    @auth_required
    def get(self, rid):
        r = genre_service.get_one(rid)
        sm_d = GenreSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self):
        data = request.json
        res = genre_service.update(data)
        return res, 201

    @admin_required
    def delete(self, gid):
        genre_service.delete(gid)
        return 'info deleted', 204
