from markitdown import MarkItDown
from openai import OpenAI

def main():
    client = OpenAI(
        base_url = 'http://localhost:11434/v1',
        api_key='ollama', # required, but unused
    )
    md = MarkItDown(llm_client=client, llm_model="minicpm-v")
    result = md.convert("../resources/test.png", llm_prompt="提取图片的文字部分，生成markdown，用中文回答")
    print(result.text_content)

if __name__ == '__main__':
    main()