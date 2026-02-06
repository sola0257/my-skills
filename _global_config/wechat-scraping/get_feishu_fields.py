import json
import requests

# 飞书配置信息
APP_ID = 'cli_a9c9443f9278dbd6'
APP_SECRET = 'Nzkl6zFqpJ1hZ6oNJgz3Se0UhQsdUst4'
APP_TOKEN = 'N42HbN11JaIxxgstE4gcRdl0nPf'
TABLE_ID = 'tbltqXWK6ozCXAXo'

# 获取 tenant_access_token
def get_tenant_access_token():
    url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    data = {
        'app_id': APP_ID,
        'app_secret': APP_SECRET
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    if result.get('code') == 0:
        return result.get('tenant_access_token')
    else:
        raise Exception(f'获取token失败: {result}')

# 获取表格字段列表
def get_table_fields(access_token):
    url = f'https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/fields'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json; charset=utf-8'
    }

    response = requests.get(url, headers=headers)
    return response.json()

# 主函数
def main():
    print('获取飞书表格字段信息...\n')

    # 1. 获取access token
    access_token = get_tenant_access_token()
    print('✓ Token获取成功\n')

    # 2. 获取字段列表
    result = get_table_fields(access_token)

    if result.get('code') == 0:
        fields = result.get('data', {}).get('items', [])
        print(f'表格共有 {len(fields)} 个字段：\n')

        for i, field in enumerate(fields, 1):
            field_name = field.get('field_name', '')
            field_type = field.get('type', '')
            field_id = field.get('field_id', '')

            print(f'{i}. 字段名: {field_name}')
            print(f'   字段ID: {field_id}')
            print(f'   字段类型: {field_type}')
            print()

        # 保存字段信息到文件
        with open('feishu_fields.json', 'w', encoding='utf-8') as f:
            json.dump(fields, f, ensure_ascii=False, indent=2)
        print('✓ 字段信息已保存到 feishu_fields.json')

    else:
        print(f'✗ 获取字段失败: {result}')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'\n✗ 错误: {str(e)}')
        import traceback
        traceback.print_exc()
