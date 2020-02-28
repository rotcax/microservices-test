from concurrent import futures
import time
import grpc

import score_pb2
import score_pb2_grpc

class ScoreServicer(score_pb2_grpc.ScoreServicer):
    def GetScore(self, request, context):
        response = score_pb2.Game(score=500)

        return response

server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))

score_pb2_grpc.add_ScoreServicer_to_server(
    ScoreServicer(),
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
