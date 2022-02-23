from importlib.resources import path
from multiprocessing import connection
from flask_restful import Resource,reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required
import sqlite3

def normalize_path_params(cidade=None,estrelas_min=0,
                            estrelas_max=5,diaria_max=10000,
                            diaria_min=0,limit=50,offset=0):
    
    if(cidade):
        return{
            'estrelas_min':estrelas_min,
            'estrelas_max':estrelas_max,
            'diaria_min':diaria_min,
            'diaria_max':diaria_max,
            'cidade':cidade,
            'limit':limit,
            'offset':offset
        }
    else:
        return{
            'estrelas_min':estrelas_min,
            'estrelas_max':estrelas_max,
            'diaria_min':diaria_min,
            'diaria_max':diaria_max,
            'limit':limit,
            'offset':offset
        }



path_params = reqparse.RequestParser()
path_params.add_argument('cidade')
path_params.add_argument('estrelas_min')
path_params.add_argument('estrelas_max')
path_params.add_argument('diaria_min')
path_params.add_argument('diaria_max')
path_params.add_argument('limit')
path_params.add_argument('offset')


class Hoteis(Resource):
    def get(self):
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()


        dados = path_params.parse_args()
        dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None}
        parametros = normalize_path_params(**dados_validos)

        if(not parametros.get('cidade')):
            consulta = 'SELECT * FROM hoteis \
                WHERE (estrelas>? and estrelas < ?)\
                    and (diaria>? and diaria<?)\
                        LIMIT ? OFFSET ?'

            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta,(tupla))
        else:
            consulta = 'SELECT * FROM hoteis \
                WHERE (estrelas>? and estrelas < ?)\
                    and (diaria>? and diaria<?)\
                        and cidade = ? LIMIT ? OFFSET ?'

            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta,(tupla))
        
        hoteis = []
        for linha in resultado:
            hoteis.append({
                'hotel_id': linha[0],
                'nome': linha[1],
                'estrelas': linha[2],
                'diaria': linha[3],
                'cidade': linha[4]
            })
        return {'hoteis':hoteis}

class Hotel(Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')
    


    def get(self,hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'msg':'Hotel not found'}, 404 #not found

    @jwt_required
    def post(self,hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {'menssage': 'hotel id já existente'},400
        
        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id,**dados)
        hotel.save_hotel()
        return hotel.json()

    @jwt_required
    def put(self,hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel_encontrado =  HotelModel.find_hotel(hotel_id)

        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(),200
        
        hotel = HotelModel(hotel_id,**dados)
        hotel.save_hotel()
        return hotel.json(),201
        
    @jwt_required
    def delete(self,hotel_id):
        hotel =  HotelModel.find_hotel(hotel_id)
        if hotel:
            hotel.delete_hotel()
            return {'msg': 'Hotel deleted'}
        return {'msg': 'Hotel not found'},404