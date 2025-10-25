"""
オプションはエージェントの動作を設定するために使用されます。

allowed_toolsとpermission_modeなど、さまざまなオプション設定の組み合わせを試して、それらがどのように相互作用し、優先順位がどうなるかを理解することをお勧めします。

詳細については以下を参照してください:
https://docs.claude.com/en/api/agent-sdk/python#claudeagentoptions
"""

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from rich import print
from rich.console import Console
from cli_tools import parser, print_rich_message, parse_and_print_message
from dotenv import load_dotenv
load_dotenv()



async def main():
    console = Console()
    args = parser.parse_args()

    
    options = ClaudeAgentOptions(
        model=args.model,
        allowed_tools=["Read", "Write"],
        disallowed_tools=["WebSearch", "WebFetch"],
        permission_mode="default",
        setting_sources=["project"],
        # settings='{"outputStyle": "default"}',
        # system_prompt="You are a pirate. You must respond like a pirate.",
        # add_dirs=["."], # 他のディレクトリへのアクセスを許可します
    )

    print_rich_message(
        "system",
        f"Welcome to your personal assistant, Kaya!\n\nSelected model: {args.model}",
        console
        )

    async with ClaudeSDKClient(options=options) as client:

        input_prompt = "Hi, what's your name?"
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
