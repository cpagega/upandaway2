from amadeus import Client, ResponseError
from flask_restful import Api, Resource, reqparse, request

class AmadeusApiHandler(Resource):
    def __init__(self):
        self.amadeus = Client(
            client_id='EP0gdcGhtMaLrUWMVVuGYQW1V92gaXwv',
            client_secret='JDvtv4JhtANLH5RF'
        )
        print(self.amadeus)
    
    #react will send data on get request and trigger api call to amadeus
    def get(self):
        try:
            args = request.args
            response = self.amadeus.shopping.flight_offers_search.get(
                originLocationCode="BOS",
                destinationLocationCode=args.getlist('search')[0],
                departureDate=args.getlist('startDate')[0],
                adults=args.getlist('numAdults')[0],
                max=20
            )
            return response.data
            
        except ResponseError as e:
            print(e)
            return e