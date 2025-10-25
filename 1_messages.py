"""
SDKからのメッセージを解析して表示する方法の例。

このファイルを簡潔にするため、cli_tools.pyからヘルパー関数をインポートしています。これにより、印刷/ロギング機能をメインのアプリケーションロジックから分離し、何が起こっているかを理解しやすくしています。
"""

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from rich import print
from rich.console import Console
from cli_tools import print_rich_message, parse_and_print_message
from dotenv import load_dotenv
load_dotenv()


MODEL = "haiku"


async def main():
    # このセッションで使用するコンソールを初期化します
    console = Console()

    options = ClaudeAgentOptions(
        model=MODEL
    )

    # 起動メッセージ
    print_rich_message(
        type="system", 
        message=f"Welcome to your Claude Personal Assistant!\n\nSelected model: {MODEL}",
        console=console
    )

    async with ClaudeSDKClient(options=options) as client:

        input_prompt = "Hi"
        print_rich_message("user", input_prompt, console)

        await client.query(input_prompt)

        async for message in client.receive_response():
            # デバッグ用に生のメッセージを表示するには、コメントを外してください
            # print(message)
            parse_and_print_message(message, console)


if __name__ == "__main__":
    import asyncio
    # これはJupyter notebook/対話型環境でasyncioを実行するために必要です
    import nest_asyncio
    nest_asyncio.apply()

    asyncio.run(main())
