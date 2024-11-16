import json
import pdb
import pika
from main import db, Blog,app

params = pika.URLParameters('amqps://hmsgdxom:Jc20Xt46mWcXLWt9Cc0WiLpt6xQKiXTw@lionfish.rmq.cloudamqp.com/hmsgdxom')
connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')


def callback(ch, method, properties, body):
    print('Received in main')
    data = json.loads(body)

    print(data)
    print(properties.content_type)

    if properties.content_type == 'blog_created':
        blog = Blog(id=data['id'], title=data['title'], content=data['content'], image=data['image'])
        db.session.add(blog)
        db.session.commit()
        print('blog Created')

    elif properties.content_type == 'blog_updated':
  
        blog = Blog.query.get(data['id'])
    
        blog.title = data['title']
        blog.content = data['content']
        db.session.commit()
        print('blog Updated')

    elif properties.content_type == 'blog_deleted':
        blog = Blog.query.get(data)
        db.session.delete(blog)
        db.session.commit()
        print('blog Deleted')


channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
