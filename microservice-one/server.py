from concurrent import futures
import time
import grpc

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

server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))

videogame_pb2_grpc.add_VideogameServicer_to_server(
    VideogameServicer(),
    server
)

print('Starting server. Listening on port 50051.')
server.add_insecure_port('[::]:50051')
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
