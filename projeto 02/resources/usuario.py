from flask_restful import Resource,reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token
from werkzeug.security import safe_str_cmp

class User(Resource):

    def get(self,user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'msg':'User not found'}, 404 #not found

    def delete(self,user_id):
        user =  UserModel.find_user(user_id)
        if user:
            user.delete_user()
            return {'msg': 'user deleted'}
        return {'msg': 'user not found'},404


class UserRegister(Resource):

    def post(self):
        atributos = reqparse.RequestParser()
        atributos.add_argument('login')
        atributos.add_argument('senha')
        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {'msg':'the login already exists'}
        
        user = UserModel(**dados)
        user.save_user()
        return {'msg':'User cread successfully!'},201

class UserLogin(Resource):
    @classmethod
    def post(cls):
        atributos = reqparse.RequestParser()
        atributos.add_argument('login')
        atributos.add_argument('senha')
        dados = atributos.parse_args()

        user = UserModel.find_by_login(dados['login'])
        if user and safe_str_cmp(user.senha,dados['senha']):
            token_de_acesso = create_access_token(identity=user.user_id)
            return {'access_token':token_de_acesso},200
        
        return {'msg':"the username or password is incorrect."},401