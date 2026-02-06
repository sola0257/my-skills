from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
from datetime import datetime
import time
import storage

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Routes

@app.route('/', methods=['GET'])
def index():
    """Root endpoint - API information"""
    return jsonify({
        'name': 'Xiaohongshu Visual Platform API',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'health': '/api/health',
            'generate': '/api/generate (POST)',
            'contents': '/api/contents (GET, POST)',
            'content_detail': '/api/contents/<id> (GET, PUT, DELETE)'
        }
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'Backend is running',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/generate', methods=['POST'])
def generate_content():
    """Generate content based on topic (mock implementation)"""
    data = request.get_json()
    topic = data.get('topic', '')

    if not topic:
        return jsonify({'error': 'Topic is required'}), 400

    # Simulate processing time
    time.sleep(2)

    # Return mock generated content
    content = {
        'id': str(len(MOCK_CONTENTS) + 1),
        'topic': topic,
        'title': f'关于{topic}的精彩内容',
        'content': f'这是关于{topic}的详细介绍。内容包含了丰富的信息和实用的建议...',
        'images': [f'https://via.placeholder.com/400x300?text=Generated+{i}' for i in range(1, 13)],
        'status': 'draft',
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }

    return jsonify(content)

@app.route('/api/contents', methods=['GET'])
def list_contents_route():
    """List all contents"""
    status_filter = request.args.get('status')
    contents = storage.list_contents(status=status_filter)
    return jsonify(contents)

@app.route('/api/contents', methods=['POST'])
def create_content():
    """Save new content"""
    data = request.get_json()

    # Validate required fields
    required_fields = ['topic', 'title', 'content']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400

    # Create content data
    content_data = {
        'topic': data['topic'],
        'title': data['title'],
        'content': data['content'],
        'images': data.get('images', []),
        'status': data.get('status', 'draft')
    }

    # Save to storage
    saved_content = storage.save_content(content_data)

    return jsonify(saved_content), 201

@app.route('/api/contents/<content_id>', methods=['GET'])
def get_content_route(content_id):
    """Get content by ID"""
    content = storage.get_content(content_id)

    if not content:
        return jsonify({'error': 'Content not found'}), 404

    return jsonify(content)

@app.route('/api/contents/<content_id>', methods=['PUT'])
def update_content(content_id):
    """Update existing content"""
    content = storage.get_content(content_id)

    if not content:
        return jsonify({'error': 'Content not found'}), 404

    data = request.get_json()

    # Update fields
    content['topic'] = data.get('topic', content['topic'])
    content['title'] = data.get('title', content['title'])
    content['content'] = data.get('content', content['content'])
    content['images'] = data.get('images', content['images'])
    content['status'] = data.get('status', content['status'])

    # Save updated content
    updated_content = storage.save_content(content)

    return jsonify(updated_content)

@app.route('/api/contents/<content_id>', methods=['DELETE'])
def delete_content_route(content_id):
    """Delete content by ID"""
    success = storage.delete_content(content_id)

    if not success:
        return jsonify({'error': 'Content not found'}), 404

    return jsonify({'message': 'Content deleted successfully'})

# Error handlers

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Run the app

if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5001))
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'

    print(f"Starting Flask server on {host}:{port}")
    print(f"Debug mode: {debug}")

    app.run(host=host, port=port, debug=debug)
