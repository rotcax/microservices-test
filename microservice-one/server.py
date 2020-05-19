from concurrent import futures
import time
import grpc
import pika
import uuid
import json

import videogame_pb2
import videogame_pb2_grpc

class VideogameServicer(videogame_pb2_grpc.VideogameServicer):

    def __init__(self):
        # The first thing we need to do is to establish a connection with RabbitMQ server.
        # We're connected now, to a broker on the local machine - hence the localhost.
        # If we wanted to connect to a broker on a different machine we'd simply specify its name or IP address here.
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()

        # Firstly, whenever we connect to Rabbit we need a fresh, empty queue. 
        # To do it we could create a queue with a random name, or, even better - let the server choose a random queue name for us.
        # We can do this by supplying empty queue parameter to queue_declare:
        # Secondly, once the consumer connection is closed, the queue should be deleted. There's an exclusive flag for that
        result = self.channel.queue_declare(queue='', exclusive=True)
        # At this point result.method.queue contains a random queue name. For example it may look like amq.gen-JzTY20BRgKO-HjmUJj0wLg.
        self.callback_queue = result.method.queue

        # We need to tell RabbitMQ that this particular callback function should receive messages from our hello queue
        # An ack(nowledgement) is sent back by the consumer to tell RabbitMQ that a particular message had been received, processed and that RabbitMQ is free to delete it.
        # https://www.rabbitmq.com/tutorials/tutorial-two-python.html

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

    def SaveVideogame(self, request, context):
        response = videogame_pb2.GameResponse(game={
            'name': request.name,
            'score': request.score
        })

        return response

    def GetVideogame(self, request, context):

        array_objects = {'name': 'Super Mario Bros','score': 200},{'name': 'Black','score': 6000}

        # Antes de enviarlo por el BUS
        print(array_objects)
        # Hacer request
        my_result = self.call(array_objects)
        # Lo recibido por el el BUS
        print(my_result)
        my_result = json.loads(my_result)
        print(my_result)


        #Aqui se devuelve la respuesta al gateway
        response = videogame_pb2.GameMultipleResponse(game=my_result)

        return response
        
    
    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, my_params):
        self.response = None
        self.corr_id = str(uuid.uuid4())

        # In order to receive a response the client needs to send a 'callback' queue address with the request. 
        self.channel.basic_publish(
            exchange='',                            # your message is delivered to the queue with a name equal to the routing key of the message. 
            routing_key='rpc_queue',                
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,       # Commonly used to name a callback queue
                correlation_id=self.corr_id,        # Useful to correlate RPC responses with requests. (Set an unique value for every request)
                content_type='application/json',    # Used to describe the mime-type of the encoding. For example for the often used JSON encoding.
            ),
            body=json.dumps(my_params)
        )

        while self.response is None:
            self.connection.process_data_events()
        return self.response

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
    
