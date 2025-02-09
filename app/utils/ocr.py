import base64

from loguru import logger
from openai import AsyncOpenAI

from app.config import config

SYSTEM_PROMPT = """
<instruction>
Your job is to OCR the image and convert it to LaTeX format.
</instruction>

<prohibited_actions>
Do not include \\documentclass, \\begin{document}, \\end{document}, or any preamble.
</prohibited_actions>

<example_math_output>
```latex
\\begin{equation}
    x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}
\\end{equation}
```
</example_math_output>

<example_text_output>
```latex
\\textbf{Hello World}
```
</example_text_output>

<example_normal_text_output>
```latex
The quick brown fox jumps over the lazy dog.
```
</example_normal_text_output>
"""

client = AsyncOpenAI(api_key=config.OPENAI_API_KEY, base_url=config.OPENAI_BASE_URL)


async def process_image(image_bytes: bytes, user_instruction: str = None, system_instruction: str = None, model: str = "gpt-4o-2024-11-20") -> str:
    try:
        if user_instruction is None:
            user_instruction = "Convert the image to LaTeX format."
        if system_instruction is None:
            system_instruction = SYSTEM_PROMPT

        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        completion = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": [
                    {"type": "text", "text": user_instruction},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                ]
                }
            ],
            temperature=0.1,
            presence_penalty=0,
            frequency_penalty=0,
            top_p=1
        )
        logger.info(f'Processed image: {completion.choices[0].message.content}')
        return completion.choices[0].message.content.replace('```latex\n', '').replace('```', '')
    except Exception as e:
        logger.error(e)
        return None
