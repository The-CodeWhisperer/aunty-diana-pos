import os
from flask import Flask, render_template, request, jsonify
import database

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def student_order_page():
    return render_template('index.html')

@app.route('/kitchen')
def kitchen_display():
    pending_orders = database.get_pending_orders()
    return render_template('kitchen.html', orders=pending_orders)

@app.route('/api/upload_order', methods=['POST'])
def upload_order():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
        
    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400
        
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename)
    audio_file.save(file_path)
    
    order_id = database.add_order(file_path)
    return jsonify({'message': 'Order placed successfully', 'order_id': order_id}), 201

@app.route('/api/complete_order/<int:order_id>', methods=['POST'])
def complete_order(order_id):
    database.update_order_status(order_id, 'completed')
    return jsonify({'message': f'Order {order_id} marked as completed'}), 200

if __name__ == '__main__':
    database.create_tables()
    app.run(debug=True, port=5000)