import grpc

import score_pb2
import score_pb2_grpc

def mygRpc():
    channel = grpc.insecure_channel('localhost:50052')
    stub = score_pb2_grpc.ScoreStub(channel)
    request = score_pb2.Empty()
    response = stub.GetScore(request)

    return response