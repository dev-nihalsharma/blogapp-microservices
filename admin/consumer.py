import json, pika, django, os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin.settings')
django.setup()

from blogs.models import Blog

params = pika.URLParameters('amqps://hmsgdxom:Jc20Xt46mWcXLWt9Cc0WiLpt6xQKiXTw@lionfish.rmq.cloudamqp.com/hmsgdxom')
connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')

def callback(ch, method, properties, body):
    print('Received in admin')
    data = json.loads(body)

    print(data)
    
    if properties.content_type == 'blog_liked':
        blog = Blog.objects.get(data['id'])
        blog.likes = blog.likes + 1
        print('Blog liked!')

channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()


