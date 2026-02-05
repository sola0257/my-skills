#!/usr/bin/env python3
"""
Feishu MCP Server
Provides MCP tools for interacting with Feishu Bitable API
"""

import os
import sys
import json
import requests
from datetime import datetime
from typing import Any, Dict, List, Optional

# MCP SDK imports
try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent
    import mcp.server.stdio
except ImportError:
    print("Error: mcp package not found. Install with: pip install mcp", file=sys.stderr)
    sys.exit(1)

# Feishu API Configuration
APP_ID = os.getenv("FEISHU_APP_ID")
APP_SECRET = os.getenv("FEISHU_APP_SECRET")

# Table configurations
TABLES = {
    "content_log": {
        "app_token": "N42HbN11JaIxxgstE4gcRdl0nPf",
        "table_id": "tbltqXWK6ozCXAXo",
        "name": "内容记录"
    },
    "product_catalog": {
        "app_token": "N42HbN11JaIxxgstE4gcRdl0nPf",
        "table_id": "tblYfRNXXeqn57q0",
        "name": "商品库"
    },
    "fans_record": {
        "app_token": "N42HbN11JaIxxgstE4gcRdl0nPf",
        "table_id": "tblgmTuHejIoWu2i",
        "name": "粉丝数记录"
    }
}

class FeishuAPI:
    """Feishu API client"""

    def __init__(self):
        self.app_id = APP_ID
        self.app_secret = APP_SECRET
        self.access_token = None
        self.token_expires_at = 0

    def get_access_token(self) -> str:
        """Get or refresh access token"""
        if self.access_token and datetime.now().timestamp() < self.token_expires_at:
            return self.access_token

        url = "https://open.feishu.cn/open-api/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }

        response = requests.post(url, json=payload)
        data = response.json()

        if data.get("code") == 0:
            self.access_token = data["tenant_access_token"]
            self.token_expires_at = datetime.now().timestamp() + data.get("expire", 7200) - 60
            return self.access_token
        else:
            raise Exception(f"Failed to get access token: {data}")

    def add_record(self, table_key: str, app_token: str, fields: Dict[str, Any]) -> Dict:
        """Add a record to a table"""
        token = self.get_access_token()
        url = f"https://open.feishu.cn/open-api/bitable/v1/apps/{app_token}/tables/{table_key}/records"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        payload = {"fields": fields}
        response = requests.post(url, headers=headers, json=payload)
        return response.json()

    def list_records(self, table_key: str, app_token: str, page_size: int = 20) -> Dict:
        """List records from a table"""
        token = self.get_access_token()
        url = f"https://open.feishu.cn/open-api/bitable/v1/apps/{app_token}/tables/{table_key}/records"

        headers = {
            "Authorization": f"Bearer {token}"
        }

        params = {"page_size": page_size}
        response = requests.get(url, headers=headers, params=params)
        return response.json()

    def update_record(self, table_key: str, app_token: str, record_id: str, fields: Dict[str, Any]) -> Dict:
        """Update a record in a table"""
        token = self.get_access_token()
        url = f"https://open.feishu.cn/open-api/bitable/v1/apps/{app_token}/tables/{table_key}/records/{record_id}"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        payload = {"fields": fields}
        response = requests.put(url, headers=headers, json=payload)
        return response.json()

# Initialize Feishu API client
feishu_api = FeishuAPI()

# Initialize MCP server
server = Server("feishu")

@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available Feishu tools"""
    return [
        Tool(
            name="feishu_add_content_record",
            description="Add a content record to Feishu content log table",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Content title"},
                    "platform": {"type": "string", "description": "Platform name (e.g., 微信公众号-订阅号, 小红书)"},
                    "content_type": {"type": "string", "description": "Content type (e.g., 长文, 图文)"},
                    "date": {"type": "string", "description": "Publish date (YYYY-MM-DD)"},
                    "file_path": {"type": "string", "description": "Local file path (optional)"}
                },
                "required": ["title", "platform", "content_type", "date"]
            }
        ),
        Tool(
            name="feishu_list_content_records",
            description="List recent content records from Feishu",
            inputSchema={
                "type": "object",
                "properties": {
                    "page_size": {"type": "number", "description": "Number of records to return (default: 20)"}
                }
            }
        ),
        Tool(
            name="feishu_add_product",
            description="Add a product to Feishu product catalog",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Product name"},
                    "category": {"type": "string", "description": "Product category"},
                    "price": {"type": "number", "description": "Product price"},
                    "stock": {"type": "number", "description": "Stock quantity"},
                    "link": {"type": "string", "description": "Product link (optional)"}
                },
                "required": ["name", "category", "price"]
            }
        ),
        Tool(
            name="feishu_update_fans_count",
            description="Update fans count for a platform",
            inputSchema={
                "type": "object",
                "properties": {
                    "platform": {"type": "string", "description": "Platform name"},
                    "fans_count": {"type": "number", "description": "Current fans count"},
                    "date": {"type": "string", "description": "Date (YYYY-MM-DD)"}
                },
                "required": ["platform", "fans_count", "date"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Any) -> List[TextContent]:
    """Handle tool calls"""

    try:
        if name == "feishu_add_content_record":
            # Convert date to timestamp
            date_str = arguments["date"]
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            timestamp = int(date_obj.timestamp() * 1000)

            fields = {
                "日期": timestamp,
                "标题": arguments["title"],
                "平台": arguments["platform"],
                "内容类型": arguments["content_type"]
            }

            if "file_path" in arguments:
                fields["本地文件路径"] = arguments["file_path"]

            table_config = TABLES["content_log"]
            result = feishu_api.add_record(
                table_config["table_id"],
                table_config["app_token"],
                fields
            )

            if result.get("code") == 0:
                return [TextContent(
                    type="text",
                    text=f"✅ Successfully added content record: {arguments['title']}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"❌ Failed to add record: {result.get('msg', 'Unknown error')}"
                )]

        elif name == "feishu_list_content_records":
            page_size = arguments.get("page_size", 20)
            table_config = TABLES["content_log"]

            result = feishu_api.list_records(
                table_config["table_id"],
                table_config["app_token"],
                page_size
            )

            if result.get("code") == 0:
                records = result.get("data", {}).get("items", [])
                output = f"Found {len(records)} content records:\n\n"

                for record in records:
                    fields = record.get("fields", {})
                    title = fields.get("标题", "N/A")
                    platform = fields.get("平台", "N/A")
                    date_ts = fields.get("日期")
                    date_str = datetime.fromtimestamp(date_ts / 1000).strftime("%Y-%m-%d") if date_ts else "N/A"

                    output += f"- [{date_str}] {title} ({platform})\n"

                return [TextContent(type="text", text=output)]
            else:
                return [TextContent(
                    type="text",
                    text=f"❌ Failed to list records: {result.get('msg', 'Unknown error')}"
                )]

        elif name == "feishu_add_product":
            fields = {
                "商品名称": arguments["name"],
                "商品分类": arguments["category"],
                "价格": arguments["price"]
            }

            if "stock" in arguments:
                fields["库存"] = arguments["stock"]
            if "link" in arguments:
                fields["商品链接"] = arguments["link"]

            table_config = TABLES["product_catalog"]
            result = feishu_api.add_record(
                table_config["table_id"],
                table_config["app_token"],
                fields
            )

            if result.get("code") == 0:
                return [TextContent(
                    type="text",
                    text=f"✅ Successfully added product: {arguments['name']}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"❌ Failed to add product: {result.get('msg', 'Unknown error')}"
                )]

        elif name == "feishu_update_fans_count":
            date_str = arguments["date"]
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            timestamp = int(date_obj.timestamp() * 1000)

            fields = {
                "日期": timestamp,
                "平台": arguments["platform"],
                "粉丝数": arguments["fans_count"]
            }

            table_config = TABLES["fans_record"]
            result = feishu_api.add_record(
                table_config["table_id"],
                table_config["app_token"],
                fields
            )

            if result.get("code") == 0:
                return [TextContent(
                    type="text",
                    text=f"✅ Successfully updated fans count for {arguments['platform']}: {arguments['fans_count']}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"❌ Failed to update fans count: {result.get('msg', 'Unknown error')}"
                )]

        else:
            return [TextContent(
                type="text",
                text=f"❌ Unknown tool: {name}"
            )]

    except Exception as e:
        return [TextContent(
            type="text",
            text=f"❌ Error: {str(e)}"
        )]

async def main():
    """Run the MCP server"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
