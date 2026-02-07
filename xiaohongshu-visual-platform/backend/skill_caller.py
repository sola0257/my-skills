"""
Skill caller module for integrating Claude Code skills
Calls xiaohongshu-content-generator skill via subprocess
"""

import subprocess
import json
import os
import re


def call_xiaohongshu_skill(topic):
    """
    Call xiaohongshu-content-generator skill to generate content

    Args:
        topic (str): The topic to generate content for

    Returns:
        dict: Generated content with title, content, and image prompts

    Raises:
        Exception: If skill execution fails
    """
    try:
        # Prepare the command to call Claude Code with the skill
        # The skill expects a topic as input
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
        # The skill should output JSON format
        output = result.stdout.strip()

        # Try to extract JSON from the output
        # Look for JSON block in the output
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

        return content_data

    except subprocess.TimeoutExpired:
        raise Exception("Skill execution timed out after 5 minutes")
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse skill output as JSON: {e}")
    except Exception as e:
        raise Exception(f"Error calling skill: {e}")
