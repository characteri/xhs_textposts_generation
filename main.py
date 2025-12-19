import streamlit as st
import os
from utils import generate_xiaohongshu

# 页面配置
st.set_page_config(page_title="爆款小红书AI写作助手", page_icon="✏️", layout="wide")

st.header("爆款小红书AI写作助手 ✏️")

with st.sidebar:
    st.header("⚙️ 配置中心")
    # 优先读取环境变量，支持手动输入覆盖
    default_api_key = os.getenv("OPENAI_API_KEY", "")
    openai_api_key = st.text_input(
        "请输入DeepSeek API密钥：",
        type="password",
        value=default_api_key,
        help="已自动读取环境变量中的密钥，可直接使用或手动修改"
    )
    st.markdown("[获取DeepSeek API密钥](https://platform.deepseek.com/)")

    # 增加模型选择（DeepSeek支持的主流模型）
    model_option = st.selectbox(
        "选择生成模型",
        ["deepseek-chat", "deepseek-coder-v2"],
        index=0,
        help="deepseek-chat适合文案创作，deepseek-coder适合技术相关主题"
    )

# 主题输入区域
theme = st.text_input(
    "📝 请输入创作主题",
    placeholder="例如：冬日平价护肤攻略、打工人高效摸鱼学习法、租房改造ins风"
)

# 高级选项（可选）
with st.expander("🔧 高级设置（可选）", expanded=False):
    writing_style = st.selectbox(
        "正文风格",
        ["亲切", "幽默", "热情", "温馨", "轻松", "真诚"],
        index=0
    )
    title_style = st.selectbox(
        "标题侧重",
        ["正面刺激", "负面刺激", "悬念提问", "热点结合"],
        index=0
    )

submit = st.button("🚀 开始写作", type="primary")

# 提交逻辑处理
if submit:
    if not openai_api_key:
        st.warning("⚠️ 请输入DeepSeek API密钥")
        st.stop()
    if not theme:
        st.warning("⚠️ 请输入生成内容的主题")
        st.stop()

    with st.spinner("AI正在努力创作中，请稍等..."):
        try:
            # 调用生成函数（传入模型参数）
            result = generate_xiaohongshu(
                theme=theme,
                openai_api_key=openai_api_key,
                model_name=model_option,
                writing_style=writing_style,
                title_style=title_style
            )

            # 展示结果
            st.divider()
            st.success("✅ 创作完成！可直接复制使用～")

            left_column, right_column = st.columns(2, gap="large")
            with left_column:
                st.markdown("### 📌 爆款标题推荐")
                for i, title in enumerate(result.titles, 1):
                    st.markdown(f"**{i}. {title}**")
                    st.markdown("---")

            with right_column:
                st.markdown("### 📝 正文内容")
                st.write(result.content)

                # 复制按钮
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("复制标题"):
                        st.write("标题已复制到剪贴板！")
                        st.code("\n".join(result.titles))
                with col2:
                    if st.button("复制正文"):
                        st.write("正文已复制到剪贴板！")
                        st.code(result.content)

        except Exception as e:
            st.error(f"❌ 创作失败：{str(e)}")
            st.info("💡 建议检查：1. API密钥是否有效 2. 网络是否能访问DeepSeek API 3. 主题是否清晰")