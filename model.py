import pika
import time
import json

def model(question):
    if question == "Hi":
        return "Hello!"
    elif question == "Alireza":
        return  "Davoodi"
    elif question == "How are you?":
        return "I am doing great actually<br/>How about you?"
    else:
        return "I Don't Know!"

def callback(ch, method, properties, body):
    question = body.decode()
    print(f"Received question: {question}")
    
    answer = model(question)
    
    response = {
        "question": question,
        "answer": {
            "time": int(time.time()),  
            "content": answer
        }
    }
    
    ch.basic_publish(exchange='', routing_key='answer', body=json.dumps(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_model_server():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    
    channel.queue_declare(queue='question')
    
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='question', on_message_callback=callback)
    
    print("Waiting for questions...")
    channel.start_consuming()

if __name__ == '__main__':
    start_model_server()

