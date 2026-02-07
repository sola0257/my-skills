"""
Skill caller module for integrating Claude Code skills
Calls xiaohongshu-content-generator skill via subprocess

Output Format Contract (v1):
{
    "title": str,        # Required: Content title
    "content": str,      # Required: Main content text
    "images": list       # Required: List of image URLs/paths or objects with {url, prompt}
}
"""

import subprocess
import json
import os
import re
from typing import Dict, Any, List


# Expected output format version
SKILL_OUTPUT_VERSION = 'v1'

# Required fields for v1 format
REQUIRED_FIELDS_V1 = ['title', 'content', 'images']


def validate_skill_output(data: Dict[str, Any], version: str = 'v1') -> None:
    """
    Validate skill output format

    Args:
        data: The parsed skill output data
        version: Expected format version

    Raises:
        ValueError: If output format is invalid
    """
    if version == 'v1':
        # Check required fields
        missing_fields = [field for field in REQUIRED_FIELDS_V1 if field not in data]
        if missing_fields:
            raise ValueError(
                f"Skill output missing required fields: {', '.join(missing_fields)}. "
                f"Expected format: {REQUIRED_FIELDS_V1}"
            )

        # Validate field types
        if not isinstance(data['title'], str):
            raise ValueError(f"Field 'title' must be string, got {type(data['title']).__name__}")

        if not isinstance(data['content'], str):
            raise ValueError(f"Field 'content' must be string, got {type(data['content']).__name__}")

        if not isinstance(data['images'], list):
            raise ValueError(f"Field 'images' must be list, got {type(data['images']).__name__}")
    else:
        raise ValueError(f"Unsupported skill output version: {version}")


def call_xiaohongshu_skill(topic: str, version: str = 'v1') -> Dict[str, Any]:
    """
    Call xiaohongshu-content-generator skill to generate content

    Args:
        topic: The topic to generate content for
        version: Expected output format version (default: 'v1')

    Returns:
        dict: Generated content with title, content, and image prompts
              Format depends on version parameter

    Raises:
        Exception: If skill execution fails
        ValueError: If output format validation fails
    """
    try:
        # Prepare the command to call Claude Code with the skill
        cmd = [
            'claude',
            'code',
            '--skill', 'xiaohongshu-content-generator',
            '--input', topic
        ]

        # Execute the command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )

        if result.returncode != 0:
            raise Exception(f"Skill execution failed: {result.stderr}")

        # Parse the output
        output = result.stdout.strip()

        # Try to extract JSON from the output
        json_match = re.search(r'\{.*\}', output, re.DOTALL)
        if json_match:
            content_data = json.loads(json_match.group())
        else:
            # If no JSON found, create a basic structure
            content_data = {
                'title': f'关于{topic}的内容',
                'content': output,
                'images': []
            }

        # Validate output format
        try:
            validate_skill_output(content_data, version)
        except ValueError as e:
            raise ValueError(
                f"Skill output format validation failed: {e}\n"
                f"This usually means the skill's output format has changed.\n"
                f"Please check the skill output or update the platform code."
            )

        return content_data

    except subprocess.TimeoutExpired:
        raise Exception("Skill execution timed out after 5 minutes")
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse skill output as JSON: {e}")
    except ValueError:
        # Re-raise validation errors as-is
        raise
    except Exception as e:
        raise Exception(f"Error calling skill: {e}")
