import grpc

import videogame_pb2
import videogame_pb2_grpc

class VideogameClient():
    with open('keys/cert.pem', 'rb') as f:
        public_key = f.read()

    credentials = grpc.ssl_channel_credentials(root_certificates=public_key)
    channel = grpc.secure_channel('localhost:50051', credentials)

    stub = videogame_pb2_grpc.VideogameStub(channel)

    def save_videogame(self):
        request = videogame_pb2.Game(
            name='League of Legends',
            score=1000
        )
        response = self.stub.SaveVideogame(request)

        return response

    def get_videogame(self):
        request = videogame_pb2.Empty()
        print('request')
        response = self.stub.GetVideogame(request)
        print('response')
        return response.game


client = VideogameClient()
#print(client.save_videogame())

print(client.get_videogame())

