from concurrent import futures
import time
import grpc
import pika
import json

import score_pb2
import score_pb2_grpc

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='rpc_queue')

class ScoreServicer(score_pb2_grpc.ScoreServicer):

    def GetScore(self, request, context):
        response = score_pb2.Game(score=500)

        return response

def on_request(ch, method, props, body):
    
    my_body = json.loads(body)
    my_body[0]['name'] = 'League of Legends'
    print(my_body)

    response = my_body

    # delivery_mode: Marks a message as persistent (with a value of 2) or transient (any other value). 
    ch.basic_publish(exchange='',
                    routing_key=props.reply_to,
                    properties=pika.BasicProperties(content_type='application/json',
                                                    delivery_mode=1,    # 2 to make message persistent (guarantee that a message won't be lost)
                                                    correlation_id = \
                                                        props.correlation_id),
                    body=json.dumps(response))
    # 
    
    ch.basic_ack(delivery_tag=method.delivery_tag)

# We might want to run more than one server process. In order to spread the load equally over multiple servers we need to set the prefetch_count setting.
channel.basic_qos(prefetch_count=1)     
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()

server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))

score_pb2_grpc.add_ScoreServicer_to_server(
    ScoreServicer(),
    server
)

print('Starting server. Listening on port 50052.')
server.add_insecure_port('[::]:50052')
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
