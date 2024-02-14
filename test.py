
import os
from openai import OpenAI

#api_key = os.environ.get("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")

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.getenv("OPENAI_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gpt-3.5-turbo",
)