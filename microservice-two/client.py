import grpc

import score_pb2
import score_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')
stub = score_pb2_grpc.ScoreStub(channel)

request = score_pb2.Empty()

response = stub.GetScore(request)

print(response)
