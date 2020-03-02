from concurrent import futures
import time
import grpc
import sys
import os

import videogame_pb2
import videogame_pb2_grpc

class VideogameServicer(videogame_pb2_grpc.VideogameServicer):
    def SaveVideogame(self, request, context):
        response = videogame_pb2.GameResponse(game={
            'name': request.name,
            'score': request.score
        })

        return response

    def GetVideogame(self, request, context):
        response = videogame_pb2.GameMultipleResponse(game=[
            {
                'name': 'Super Mario Bros',
                'score': 200
            },
            {
                'name': 'Black',
                'score': 6000
            }
        ])

        return response

with open('keys/private.key', 'rb') as f:
    private_key = f.read()

with open('keys/cert.pem', 'rb') as f:
    public_key = f.read()

server_credentials = grpc.ssl_server_credentials(
    ((private_key, public_key),)
)

server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))

videogame_pb2_grpc.add_VideogameServicer_to_server(
    VideogameServicer(),
    server
)

print('Starting server. Listening on port 50051.')
server.add_secure_port('[::]:50051', server_credentials)
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
