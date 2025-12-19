##这个文件用Pydantic定义了一个 “小红书文案” 的数据结构模板，强制要求 AI 生成的结果必须符合这个格式。

from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List

class Xiaohongshu(BaseModel):
    """小红书文案数据结构模板"""
    titles: List[str] = Field(
        description="小红书的5个标题，每个20字以内，含emoji",
        min_items=5,
        max_items=5
    )
    content: str = Field(
        description="小红书正文，含emoji和tag，600字以内",
        max_length=800
    )