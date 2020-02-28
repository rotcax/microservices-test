import grpc

import videogame_pb2
import videogame_pb2_grpc

class VideogameClient():
    channel = grpc.insecure_channel('localhost:50051')
    stub = videogame_pb2_grpc.VideogameStub(channel)

    def save_videogame(self):
        request = videogame_pb2.Game(
            name='Darkness Rise',
            score=300
        )
        response = self.stub.SaveVideogame(request)

        return response

    def get_videogame(self):
        request = videogame_pb2.Empty()
        response = self.stub.GetVideogame(request)

        return response

client = VideogameClient()
print(client.save_videogame())
print(client.get_videogame())
