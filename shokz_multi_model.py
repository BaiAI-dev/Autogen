import os
import autogen

# ================= 1. 为每个Agent配置不同的模型 =================

# 配置1：DeepSeek（擅长深度推理，给健康专家用）
deepseek_config = [{
    "model": "deepseek-chat",
    "api_key": os.environ.get("DEEPSEEK_API_KEY"),
    "base_url": "https://api.deepseek.com"
}]

# 配置2：通义千问（响应快、成本低，给设备专家用）
# ⚠️ 注意：请确认下方的 base_url 是你阿里云百炼控制台里专属的地址，且末尾不要带 /chat/completions
qwen_config = [{
    "model": "qwen-turbo",
    "api_key": os.environ.get("DASHSCOPE_API_KEY"),
    "base_url": "https://ws-s8v0o45wei5767al.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
}]

# 配置3：智谱GLM（逻辑清晰，给总结协调官用）
glm_config = [{
    "model": "glm-4-flash",
    "api_key": os.environ.get("ZHIPU_API_KEY"),
    "base_url": "https://open.bigmodel.cn/api/paas/v4"
}]

# 通用参数：关闭缓存，保证真实调用
base_llm_config = {"timeout": 120, "cache_seed": None}

# ================= 2. 定义角色（Agent） =================

# 用户代理：发起需求
user_proxy = autogen.UserProxyAgent(
    name="User_Proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=1,
    is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""),
    code_execution_config=False,
)

# 健康专家：使用 DeepSeek
health_expert = autogen.AssistantAgent(
    name="Health_Expert_DeepSeek",
    system_message="""你是一个专业的运动健康顾问。用户说他膝盖疼，外面气温32度。请从健康角度给出明确的运动建议。要求：给出具体建议（是否建议跑步，替代运动方案），字数控制在80字以内。""",
    llm_config={**base_llm_config, "config_list": deepseek_config},
)

# 设备专家：使用 通义千问
device_expert = autogen.AssistantAgent(
    name="Device_Expert_Qwen",
    system_message="""你是韶音（Shokz）的资深产品专家。用户使用的是 OpenComm2（骨传导通讯耳机）。请结合产品特性（IP55防水、骨传导、续航、通话降噪），针对用户的情况给出设备使用建议。字数控制在80字以内。""",
    llm_config={**base_llm_config, "config_list": qwen_config},
)

# 协调官：使用 智谱GLM
coordinator = autogen.AssistantAgent(
    name="Coordinator_GLM",
    system_message="""你是一个决策整合助手。请阅读 Health_Expert 和 Device_Expert 的意见，整合成一段简洁的最终建议发给用户。输出格式必须包含【最终建议】。最后必须加上 'TERMINATE' 表示任务结束。""",
    llm_config={**base_llm_config, "config_list": glm_config},
)

# ================= 3. 组建多模型群聊（强制轮流发言） =================
# 注意：只把三个专家放进群聊，user_proxy 负责发起，不参与轮询
groupchat = autogen.GroupChat(
    agents=[health_expert, device_expert, coordinator], 
    messages=[],
    max_round=5, # 最多5轮
    speaker_selection_method="round_robin" # 关键：强制按顺序轮流发言
)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config={**base_llm_config, "config_list": glm_config})

# ================= 4. 发起业务咨询 =================
print("🚀 开始多模型专家会诊...")
user_proxy.initiate_chat(
    manager,
    message="我戴着 OpenComm2 准备出去跑步，但我今天膝盖有点疼，外面气温32度，我该怎么安排？",
)