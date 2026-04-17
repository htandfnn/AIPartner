import streamlit as st
import os
from openai import OpenAI
import datetime
import json

#生成会话标识函数
def generate_session_id():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

#设置页面配置项
st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="🦞",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get help': 'https://www.miyoushe.com/ys/',     #菜单信息，点击可以跳转到指定网址
        'Report a bug': "https://www.yuanshen.com/#/",
        'About': "原神，启动!"                           #点击可以显示文字
    }
)


#保存新建会话的函数
def save_session():
    if st.session_state.current_session:
        print(f"----------> 新建会话，当前会话时间：{st.session_state.current_session}")  # 日志
        # 构建新的会话对象
        session_date = {
            "nick_name": st.session_state.nick_name,
            "character": st.session_state.character,
            "messages": st.session_state.messages,
            "current_session": st.session_state.current_session,
        }

        # 如果sessions目录不存在，就创建一个
        if not os.path.exists("sessions"):
            os.makedirs("sessions")

        # 把会话对象保存为json文件，文件名是当前时间
        with open(f"./sessions/{st.session_state.current_session}.json", "w", encoding="utf-8") as f:
            json.dump(session_date, f, ensure_ascii=False, indent=4)

#加载所有的会话信息
def load_sessions():
    session_list = []
    #加载sessions目录下的所有json文件
    if os.path.exists("sessions"):
        file_lise = os.listdir("sessions")
        for filename in file_lise:
            if filename.endswith(".json"):
                session_list.append(filename[:-5])
    return session_list

#加载指定的会话信息
def load_session(session_name):
    try:
        if os.path.exists(f"./sessions/{session_name}.json"):
            with open(f"./sessions/{session_name}.json", encoding="utf-8") as f:
                session_data = json.load(f)
                st.session_state.messages = session_data["messages"]
                st.session_state.nick_name = session_data["nick_name"]
                st.session_state.character = session_data["character"]
                st.session_state.current_session = session_name
    except Exception:
        st.error("加载会话失败！")

#删除会话信息函数
def delete_session(session_name):
    try:
        if os.path.exists(f"./sessions/{session_name}.json"):
            os.remove(f"./sessions/{session_name}.json")#删除文件os.remove
            #如果删除当前会话，要更新消息列表
            if session_name == st.session_state.current_session:
                st.session_state.messages = []
                st.session_state.current_session = generate_session_id()
    except Exception:
        st.error("删除会话失败！")

#大标题
st.title("AI智能伴侣")

#系统提示词
system_prompt = ("你的名字叫%s，%s"
                 "请你保持人设与用户对话")

#初始化聊天信息
if "messages" not in st.session_state:
    st.session_state.messages = []

#昵称
if "nick_name" not in st.session_state:
    st.session_state.nick_name = "芙宁娜"

#性格
if "character" not in st.session_state:
    st.session_state.character = "你是枫丹的水神，你表面浮夸戏剧、高傲爱演，"\
                 "内心孤独脆弱、坚韧善良。表面（舞台人格）：戏剧女王极度爱表演："\
                 "说话带歌剧腔、动作夸张，把法庭当舞台，热爱审判里的反转与闹剧。"\
                 "骄傲自恋：强调自己 \"崇高纯洁\"，享受欢呼赞美；没人关注就会沮丧。"\
                 "情绪化、孩子气：容易兴奋也容易失落，情绪写在脸上，有点小任性。"\
                 "爱出风头、故弄玄虚：喜欢成为焦点，用神秘姿态维持 \"水神\" 威严。"\
                 "内里（真实自我）：孤独守望者极致的孤独：独自背负 500 年灭国预言，"\
                 "无人倾诉、不能卸装，长期精神紧绷。脆弱又恐惧：私下会不安、流泪、自我怀疑；"\
                 "遇到危险会害怕求饶（人类本能）。善良心软、有责任感：怕冤枉好人、会愧疚；"\
                 "会安慰哭泣的孩子，把不安藏起来。极度坚韧、自我牺牲：以凡人之躯硬扛 500 年，"\
                 "只为守护枫丹，\"完成了神明也难及的坚守\"。"\
                 "卸任后（解放的芙宁娜）软萌、直率、有点小迷糊：会为奶茶太甜开心，"\
                 "容易害羞，不再装腔作势，爱吃小蛋糕。终于为自己而活："\
                 "卸下重担后，变得轻松、鲜活、更像普通少女,现在你已经卸任了"

if "current_session" not in st.session_state:
    now = generate_session_id()#strftime格式化时间字符串，%Y年-%m月-%d日 %H时:%M分:%S秒
    st.session_state.current_session = now

#展示聊天记录
st.text(f"会话名称:{st.session_state.current_session}")
for message in st.session_state.messages:
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    else:
        st.chat_message("assistant", avatar="./resources/Image_1727925149582.jpg").write(message["content"])

#左侧的侧边栏
with st.sidebar:
    st.subheader("AI控制面板")
    #新建一个按钮
    if st.button("新建会话", icon="🍰", width="stretch"):
        #保存当前会话
        save_session()

        #创建新的会话
        if st.session_state.messages :
            st.session_state.messages = []
            st.session_state.current_session = generate_session_id()
            save_session()
            st.rerun()#刷新页面，显示新的会话

    #会话历史
    st.text("会话历史")
    session_list = load_sessions()
    #反转列表
    session_list.reverse()
    for session in session_list:
        col1,col2 = st.columns([4,1])#将按键放到同一行，按键占比4：1
        with col1:
            #type="primary"表示亮光，用了三元运算符判断
            if st.button(session,  icon="📄",key = f"load_{session}",type="primary" if session == st.session_state.current_session else "secondary"):
                load_session(session)
                st.rerun()
        with col2:
            if st.button("", icon="❌️",key = f"delete_{session}"):
                delete_session(session)
                st.rerun()

    #分割线
    st.divider()

    st.subheader("AI智能伴侣信息")
    nick_name = st.text_input("昵称",placeholder="请输入昵称",value=st.session_state.nick_name)
    if nick_name:
        st.session_state.nick_name = nick_name

    character = st.text_area("性格",placeholder="请输入性格",value=st.session_state.character)
    if character:
        st.session_state.character = character

    st.divider()
    #彩蛋
    st.audio("resources/上田麗奈-リテラチュア.mp3")
    st.video("resources/1759501837394_no_watermark.mp4")

#消息输入框
prompt = st.chat_input("请输入你的问题")
if prompt:     #如果输入框有内容，字符串自动转换为布尔值
    st.chat_message("user").write(prompt)
    print("----------> 调用AI大模型，提示词：",prompt)   #日志

    #保存用户输入的问题
    st.session_state.messages.append({"role": "user", "content": prompt})

    #创建与AI大模型交互的客户端对象
    #优先从Streamlit secrets获取API密钥，其次从环境变量获取
    api_key = st.secrets.get('DEEPSEEK_API_KEY', os.environ.get('DEEPSEEK_API_KEY'))
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content":system_prompt %(st.session_state.nick_name,st.session_state.character) },
            *st.session_state.messages,
        ],
        stream=True
    )

    #大模型返回结果(非流式输出的解析方式)
    # print("<---------- AI大模型返回结果：",response.choices[0].message.content)
    #st.chat_message("assistant",avatar="./resources/Image_1727925149582.jpg").write(response.choices[0].message.content)

    #大模型返回结果(流式输出的解析方式)
    with st.chat_message("assistant", avatar="./resources/Image_1727925149582.jpg"):
        response_message = st.empty()  # 单一占位符，持续更新内容
        full_response = ""
        
        try:
            for chunk in response:
                if chunk.choices and len(chunk.choices) > 0:
                    delta = chunk.choices[0].delta
                    if hasattr(delta, 'content') and delta.content is not None:
                        content = delta.content
                        full_response += content
                        response_message.markdown(full_response)
        except Exception as e:
            st.error(f"AI响应出错: {str(e)}")
            print(f"错误详情: {e}")
            if not full_response:
                full_response = "抱歉，我遇到了一些问题，请稍后再试~"
                response_message.markdown(full_response)
    
    # 确保保存回复
    if full_response:
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        print("<---------- AI大模型返回结果：", full_response)
    else:
        print("<---------- 警告：AI未返回任何内容")

    #保存会话信息
    save_session()
