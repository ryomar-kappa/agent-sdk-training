"""
Claude Agent SDKを使用したクエリの基本例

一回限りの質問、独立したタスク、毎回新しいセッションには `query()` を使用してください。
継続的な会話やステートフルなセッションには `ClaudeSDKClient` を使用してください。

詳細については以下を参照してください:
https://docs.claude.com/en/api/agent-sdk/python#choosing-between-query-and-claudesdkclient
"""

from claude_agent_sdk import query, ClaudeSDKClient, ClaudeAgentOptions
from rich import print
from dotenv import load_dotenv
load_dotenv()


MODEL="haiku"


async def main():
    # ClaudeAgentOptionsを使用してエージェントの動作を設定します。詳細は後ほど説明します
    # ここでは単純により安価なモデルに切り替えています
    options = ClaudeAgentOptions(
        model=MODEL,
    )

    # ----------------------------
    # 1. `query()` を使用した例
    # ----------------------------

    input_prompt = "Hi"
    print(f"User: {input_prompt}")

    print("Example using `query()`")
    async for message in query(prompt=input_prompt, options=options):
        print(message)

    # ----------------------------
    # 2. `ClaudeSDKClient` を使用した例
    # ----------------------------

    print(30*"=")
    print("Example using `ClaudeSDKClient`")
    # 2.1 コンテキストマネージャーを使用して、適切なクリーンアップで接続と切断を処理します
    async with ClaudeSDKClient(options=options) as client:

        # 2.2. クエリを送信します
        await client.query(input_prompt)

        # 2.3 ResultMessageを含むメッセージを受信します
        async for message in client.receive_response():
            # メッセージタイプについては以下を参照してください:
            # https://docs.claude.com/en/api/agent-sdk/python#message-types
            print(message) 

    # 切断後、クエリを再実行すると新しいセッションと会話が開始されます。

if __name__ == "__main__":
    import asyncio
    # これはJupyter notebook/対話型環境でasyncioを実行するために必要です
    import nest_asyncio
    nest_asyncio.apply()

    asyncio.run(main())