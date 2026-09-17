# 基于AutoGen的多模型协作Demo（韶音运动场景）

## 📖 项目简介
本项目基于 Microsoft AutoGen 框架，结合韶音（Shokz）的真实业务场景，构建了一个“运动健康+设备专家”的多智能体协作系统。
用户提问：“我戴着 OpenComm2 准备出去跑步，但我今天膝盖有点疼，外面气温32度，我该怎么安排？”

## 🏗️ 多模型路由架构
- **Health_Expert (DeepSeek)**：负责深度推理健康状态，给出运动建议。
- **Device_Expert (通义千问)**：负责快速响应设备特性（IP55防水、骨传导）。
- **Coordinator (智谱GLM)**：负责逻辑汇总，融合两份意见，输出最终方案。

## 🚀 核心特性
1. **混合模型调用**：打破了单模型限制，根据任务特性分配不同底层大模型。
2. **顺序协作**：利用 `speaker_selection_method="round_robin"` 确保每个专家都能充分发言，防止对话发散。
3. **真实业务验证**：模拟了高温+膝盖不适条件下的耳机使用决策流程。

## 🛠️ 本地运行
pip install pyautogen==0.2.35 -i https://pypi.tuna.tsinghua.edu.cn/simple
export DEEPSEEK_API_KEY="sk-xxx"
export DASHSCOPE_API_KEY="sk-xxx"
export ZHIPU_API_KEY="xxx"
python shokz_multi_model.py