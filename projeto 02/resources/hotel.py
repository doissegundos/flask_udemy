from flask_restful import Resource,reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required

hoteis = [
    {
        'hotel_id':'alpha',
        'nome': 'Aplha Hotel',
        'estrelas':4.3,
        'diaria': 420.34,
        'cidade': 'Rio de Janeiro'
    },
    {
        'hotel_id':'bravo',
        'nome': 'Bravo Hotel',
        'estrelas':4.4,
        'diaria': 480,
        'cidade': 'Santa Catarina'
    },
    {
        'hotel_id':'charlie',
        'nome': 'Charlie Hotel',
        'estrelas':3.9,
        'diaria': 320,
        'cidade': 'Sao Paulo'
    }
]



class Hoteis(Resource):
    def get(self):
        return {'hoteis':[hotel.json() for hotel in HotelModel.query.all()]}

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