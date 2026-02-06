from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
from datetime import datetime
import time

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Mock data for testing
MOCK_CONTENTS = [
    {
        'id': '1',
        'topic': '多肉植物养护指南',
        'title': '新手必看！多肉植物养护的5个关键技巧',
        'content': '多肉植物以其可爱的外形和易养护的特点深受喜爱。今天分享5个关键养护技巧，让你的多肉健康成长！',
        'images': [f'https://via.placeholder.com/400x300?text=Image+{i}' for i in range(1, 13)],
        'status': 'published',
        'created_at': '2024-01-15T10:30:00',
        'updated_at': '2024-01-15T10:30:00'
    },
    {
        'id': '2',
        'topic': '室内绿植推荐',
        'title': '适合新手的10种室内绿植',
        'content': '想要在家里养些绿植，但不知道从哪里开始？这10种植物非常适合新手！',
        'images': [f'https://via.placeholder.com/400x300?text=Plant+{i}' for i in range(1, 13)],
        'status': 'draft',
        'created_at': '2024-01-14T15:20:00',
        'updated_at': '2024-01-14T15:20:00'
    },
    {
        'id': '3',
        'topic': '春季养花技巧',
        'title': '春天来了！这些养花技巧你一定要知道',
        'content': '春季是植物生长的黄金时期，掌握这些技巧让你的花卉更加茂盛！',
        'images': [f'https://via.placeholder.com/400x300?text=Spring+{i}' for i in range(1, 13)],
        'status': 'published',
        'created_at': '2024-01-13T09:00:00',
        'updated_at': '2024-01-13T09:00:00'
    }
]

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
def list_contents():
    """List all contents"""
    return jsonify(MOCK_CONTENTS)

@app.route('/api/contents', methods=['POST'])
def create_content():
    """Save new content"""
    data = request.get_json()

    # Validate required fields
    required_fields = ['topic', 'title', 'content']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400

    # Create new content
    new_content = {
        'id': str(len(MOCK_CONTENTS) + 1),
        'topic': data['topic'],
        'title': data['title'],
        'content': data['content'],
        'images': data.get('images', []),
        'status': data.get('status', 'draft'),
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }

    MOCK_CONTENTS.append(new_content)

    return jsonify(new_content), 201

@app.route('/api/contents/<content_id>', methods=['GET'])
def get_content(content_id):
    """Get content by ID"""
    content = next((c for c in MOCK_CONTENTS if c['id'] == content_id), None)

    if not content:
        return jsonify({'error': 'Content not found'}), 404

    return jsonify(content)

@app.route('/api/contents/<content_id>', methods=['PUT'])
def update_content(content_id):
    """Update existing content"""
    content = next((c for c in MOCK_CONTENTS if c['id'] == content_id), None)

    if not content:
        return jsonify({'error': 'Content not found'}), 404

    data = request.get_json()

    # Update fields
    content['topic'] = data.get('topic', content['topic'])
    content['title'] = data.get('title', content['title'])
    content['content'] = data.get('content', content['content'])
    content['images'] = data.get('images', content['images'])
    content['status'] = data.get('status', content['status'])
    content['updated_at'] = datetime.now().isoformat()

    return jsonify(content)

@app.route('/api/contents/<content_id>', methods=['DELETE'])
def delete_content(content_id):
    """Delete content by ID"""
    global MOCK_CONTENTS

    content = next((c for c in MOCK_CONTENTS if c['id'] == content_id), None)

    if not content:
        return jsonify({'error': 'Content not found'}), 404

    MOCK_CONTENTS = [c for c in MOCK_CONTENTS if c['id'] != content_id]

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
