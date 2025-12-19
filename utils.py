from prompt_template import system_template_text, user_template_text
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from xiaohongshu_model import Xiaohongshu


def generate_xiaohongshu(
        theme: str,
        openai_api_key: str,
        model_name: str = "deepseek-chat",
        writing_style: str = "亲切",
        title_style: str = "正面刺激"
) -> Xiaohongshu:
    """
    调用DeepSeek API生成小红书文案
    :param theme: 创作主题
    :param openai_api_key: DeepSeek API密钥
    :param model_name: 模型名称（deepseek-chat/deepseek-coder-v2）
    :param writing_style: 正文风格
    :param title_style: 标题侧重方向
    :return: 符合Xiaohongshu模型的结果
    """
    # 配置DeepSeek模型
    llm = ChatOpenAI(
        model=model_name,
        api_key=openai_api_key,
        openai_api_base="https://api.deepseek.com/v1",  # DeepSeek官方API地址
        temperature=0.7,  # 保留创作灵活性
        max_tokens=1500  # 足够生成标题+正文
    )

    # 输出解析器
    output_parser = PydanticOutputParser(pydantic_object=Xiaohongshu)

    # 构建提示词
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_template_text),
        ("user", user_template_text)
    ])

    # 构建执行链
    chain = prompt | llm | output_parser

    # 调用模型
    result = chain.invoke({
        "parser_instructions": output_parser.get_format_instructions(),
        "theme": theme,
        "writing_style": writing_style,
        "title_style": title_style
    })

    return result