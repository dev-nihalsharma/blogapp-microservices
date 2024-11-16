
import json
import pika

params = pika.URLParameters('amqps://hmsgdxom:Jc20Xt46mWcXLWt9Cc0WiLpt6xQKiXTw@lionfish.rmq.cloudamqp.com/hmsgdxom')
connection = pika.BlockingConnection(params)

channel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method)

    channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body), properties=properties)

    
