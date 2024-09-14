from flask import Flask, render_template, request, jsonify
import pika
import json

app = Flask(__name__)

def get_rabbitmq_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    return connection, channel

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_question', methods=['POST'])
def send_question():
    user_question = request.json['question']
    
    connection, channel = get_rabbitmq_connection()
    
    channel.queue_declare(queue='question')
    channel.basic_publish(exchange='', routing_key='question', body=user_question)
    
    connection.close()
    
    return jsonify({"status": "Question sent to model!"})

@app.route('/get_answer', methods=['GET'])
def get_answer():
    connection, channel = get_rabbitmq_connection()
    
    channel.queue_declare(queue='answer')
    
    method_frame, header_frame, body = channel.basic_get(queue='answer')
    
    if method_frame:
        channel.basic_ack(method_frame.delivery_tag)
        connection.close()
        
        response = json.loads(body.decode())
        return jsonify(response)  
        
    else:
        connection.close()
        return jsonify({"answer": "No answer yet"})

if __name__ == '__main__':
    app.run(debug=True)

