#!/usr/bin/env python3
"""
Skill Output Format Validator

Validates that xiaohongshu-content-generator skill output matches
the expected format contract (v1).

Usage:
    python validate_skill_output.py <topic>
    python validate_skill_output.py "多肉植物养护"

This script will:
1. Call the skill with the given topic
2. Validate the output format
3. Report any format violations
"""

import subprocess
import json
import sys
import re
from typing import Dict, Any


# Expected format version
EXPECTED_VERSION = 'v1'

# Required fields for v1
REQUIRED_FIELDS = ['title', 'content', 'images']


def validate_output_format(data: Dict[str, Any]) -> tuple[bool, list[str]]:
    """
    Validate skill output format

    Returns:
        (is_valid, errors): Tuple of validation result and error messages
    """
    errors = []

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"❌ Missing required field: '{field}'")

    # Check field types
    if 'title' in data and not isinstance(data['title'], str):
        errors.append(f"❌ Field 'title' must be string, got {type(data['title']).__name__}")

    if 'content' in data and not isinstance(data['content'], str):
        errors.append(f"❌ Field 'content' must be string, got {type(data['content']).__name__}")

    if 'images' in data and not isinstance(data['images'], list):
        errors.append(f"❌ Field 'images' must be list, got {type(data['images']).__name__}")

    return (len(errors) == 0, errors)


def call_skill(topic: str) -> tuple[bool, Any]:
    """
    Call xiaohongshu-content-generator skill

    Returns:
        (success, data): Tuple of success status and parsed data or error message
    """
    try:
        cmd = [
            'claude',
            'code',
            '--skill', 'xiaohongshu-content-generator',
            '--input', topic
        ]

        print(f"🔄 Calling skill with topic: '{topic}'...")
        print(f"   Command: {' '.join(cmd)}")
        print()

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode != 0:
            return (False, f"Skill execution failed: {result.stderr}")

        output = result.stdout.strip()

        # Try to extract JSON
        json_match = re.search(r'\{.*\}', output, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            return (True, data)
        else:
            return (False, "No JSON found in skill output")

    except subprocess.TimeoutExpired:
        return (False, "Skill execution timed out after 5 minutes")
    except json.JSONDecodeError as e:
        return (False, f"Failed to parse JSON: {e}")
    except Exception as e:
        return (False, f"Error: {e}")


def print_validation_result(is_valid: bool, errors: list[str], data: Dict[str, Any]):
    """Print validation results in a formatted way"""
    print("=" * 70)
    print("📋 VALIDATION RESULT")
    print("=" * 70)
    print()

    if is_valid:
        print("✅ OUTPUT FORMAT IS VALID")
        print()
        print("Output structure:")
        print(f"  - title: {type(data['title']).__name__} ({len(data['title'])} chars)")
        print(f"  - content: {type(data['content']).__name__} ({len(data['content'])} chars)")
        print(f"  - images: {type(data['images']).__name__} ({len(data['images'])} items)")
        print()
        print("✅ This output is compatible with xiaohongshu-visual-platform")
    else:
        print("❌ OUTPUT FORMAT IS INVALID")
        print()
        print("Errors found:")
        for error in errors:
            print(f"  {error}")
        print()
        print("⚠️  This output will cause errors in xiaohongshu-visual-platform")
        print()
        print("Action required:")
        print("  1. Fix the skill output format")
        print("  2. OR update platform code to handle new format")
        print("  3. Read: xiaohongshu-visual-platform/docs/skill-output-format.md")

    print()
    print("=" * 70)


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_skill_output.py <topic>")
        print("Example: python validate_skill_output.py '多肉植物养护'")
        sys.exit(1)

    topic = sys.argv[1]

    print("=" * 70)
    print("🔍 SKILL OUTPUT FORMAT VALIDATOR")
    print("=" * 70)
    print()
    print(f"Expected format version: {EXPECTED_VERSION}")
    print(f"Required fields: {', '.join(REQUIRED_FIELDS)}")
    print()

    # Call skill
    success, result = call_skill(topic)

    if not success:
        print(f"❌ Failed to call skill: {result}")
        sys.exit(1)

    print("✅ Skill executed successfully")
    print()

    # Validate format
    is_valid, errors = validate_output_format(result)

    # Print results
    print_validation_result(is_valid, errors, result)

    # Exit with appropriate code
    sys.exit(0 if is_valid else 1)


if __name__ == '__main__':
    main()
