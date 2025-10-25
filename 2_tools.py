"""
ツールの使用はClaudeAgentOptionsで管理されます。

カスタムツールを追加するには3つのステップがあります:
1. ツール関数を定義する
2. ツールを使用してSDK MCPサーバーを作成する
3. ローカルMCPサーバーでエージェントを設定する

ツール名の規則は `mcp__<server_name>__<tool_name>` です。

詳細については以下を参照してください:
https://docs.claude.com/en/api/agent-sdk/custom-tools
"""

from claude_agent_sdk import tool, create_sdk_mcp_server, ClaudeSDKClient, ClaudeAgentOptions
from rich import print
from rich.console import Console
from cli_tools import parser, print_rich_message, parse_and_print_message
from typing import Any
import json
import os
from dotenv import load_dotenv
load_dotenv()


# ----------------------------
# 1. カスタムツールを定義する
# ----------------------------

@tool("search_products", "Search for products in the space toys catalog", {"query": str})
async def search_products(args: dict[str, Any]) -> dict[str, Any]:
    # JSONファイルから商品を読み込みます
    products_file = os.path.join("db", "products.json")

    try:
        with open(products_file, 'r') as f:
            products = json.load(f)
    except FileNotFoundError:
        return {
            "content": [{
                "type": "text",
                "text": "Products catalog not found."
            }]
        }

    query = args['query'].lower()
    query_words = query.split()

    # シンプルな検索: 名前またはカテゴリでクエリに一致する商品を見つけます
    matching_products = []
    for product in products:
        if any(word in product['name'].lower() for word in query_words) or any(word in product['category'].lower() for word in query_words):
            matching_products.append(product)

    if not matching_products:
        return {
            "content": [{
                "type": "text",
                "text": f"No products found matching '{args['query']}'"
            }]
        }

    # 最も関連性の高い商品を返します（簡略化のため最初のマッチ）
    best_match = matching_products[0]
    stock_status = "In Stock" if best_match['in_stock'] else "Out of Stock"

    return {
        "content": [{
            "type": "text",
            "text": f"Product: {best_match['name']}\nCategory: {best_match['category']}\nPrice: ${best_match['price']}\nStock: {stock_status}"
        }]
    }

# ----------------------------
# 2. カスタムツールを使用してSDK MCPサーバーを作成する
# ----------------------------

products_server = create_sdk_mcp_server(
    name="products",
    version="1.0.0",
    tools=[search_products]
)


async def main():
    console = Console()
    args = parser.parse_args()

    # ----------------------------
    # 3. ローカルMCPサーバーでエージェントを設定する
    # ----------------------------
    
    options = ClaudeAgentOptions(
        model=args.model,
        mcp_servers={"products": products_server},
        # すべてのデフォルトツールについては以下を参照してください:
        # https://docs.claude.com/en/api/agent-sdk/python#tool-input%2Foutput-types
        allowed_tools=["Read", "Write", "mcp__products__search_products"],
        disallowed_tools=["WebSearch", "WebFetch"]
    )

    print_rich_message(
        "system",
        f"Welcome to your Space Toys Store Assistant!\n\nSelected model: {args.model}",
        console
        )

    async with ClaudeSDKClient(options=options) as client:

        input_prompt = "Find me a telescope for kids"
        print_rich_message("user", input_prompt, console)

        await client.query(input_prompt)

        async for message in client.receive_response():
            # デバッグ用に生のメッセージを表示するには、コメントを外してください
            # print(message)
            parse_and_print_message(message, console)


if __name__ == "__main__":
    import asyncio
    import nest_asyncio
    nest_asyncio.apply()

    asyncio.run(main())
