"""
Data storage module for Xiaohongshu Visual Platform
Handles JSON file persistence for content and images
"""

import json
import os
import uuid
from datetime import datetime
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data'
CONTENTS_DIR = DATA_DIR / 'contents'
IMAGES_DIR = DATA_DIR / 'images'

# Ensure directories exist
CONTENTS_DIR.mkdir(parents=True, exist_ok=True)
IMAGES_DIR.mkdir(parents=True, exist_ok=True)


def generate_id():
    """Generate a unique ID for content"""
    return str(uuid.uuid4())


def save_content(content_data):
    """
    Save content to JSON file

    Args:
        content_data (dict): Content data with keys: title, content, images, status, etc.

    Returns:
        dict: Saved content with id and timestamps
    """
    # Generate ID if not provided
    if 'id' not in content_data:
        content_data['id'] = generate_id()

    # Add timestamps
    now = datetime.now().isoformat()
    if 'created_at' not in content_data:
        content_data['created_at'] = now
    content_data['updated_at'] = now

    # Save to file
    file_path = CONTENTS_DIR / f"{content_data['id']}.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(content_data, f, ensure_ascii=False, indent=2)

    return content_data


def get_content(content_id):
    """
    Get content by ID

    Args:
        content_id (str): Content ID

    Returns:
        dict: Content data or None if not found
    """
    file_path = CONTENTS_DIR / f"{content_id}.json"
    if not file_path.exists():
        return None

    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def list_contents(status=None):
    """
    List all contents, optionally filtered by status

    Args:
        status (str, optional): Filter by status ('draft', 'published')

    Returns:
        list: List of content data
    """
    contents = []

    for file_path in CONTENTS_DIR.glob('*.json'):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
                # Filter by status if provided
                if status is None or content.get('status') == status:
                    contents.append(content)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            continue

    # Sort by updated_at (newest first)
    contents.sort(key=lambda x: x.get('updated_at', ''), reverse=True)
    return contents


def delete_content(content_id):
    """
    Delete content by ID

    Args:
        content_id (str): Content ID

    Returns:
        bool: True if deleted, False if not found
    """
    file_path = CONTENTS_DIR / f"{content_id}.json"
    if not file_path.exists():
        return False

    file_path.unlink()
    return True


def save_image(image_data, filename=None):
    """
    Save image to images directory

    Args:
        image_data (bytes): Image binary data
        filename (str, optional): Filename, will generate if not provided

    Returns:
        str: Relative path to saved image
    """
    if filename is None:
        filename = f"{generate_id()}.png"

    file_path = IMAGES_DIR / filename
    with open(file_path, 'wb') as f:
        f.write(image_data)

    # Return relative path from data directory
    return f"images/{filename}"
