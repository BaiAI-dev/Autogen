# 1. 借一个带 Python 3.10 的底座
FROM python:3.10-slim

# 2. 在集装箱里建个文件夹叫 /app
WORKDIR /app

# 3. 先复制依赖清单，这样能利用 Docker 缓存，装得快
COPY requirements.txt .

# 4. 安装 Python 库
RUN pip install --no-cache-dir -r requirements.txt

# 5. 把剩下的代码全复制进去
COPY . .

# 6. 集装箱启动时，运行你的主程序（注意这里的名字要和你左边文件名一模一样）
CMD ["python", "shokz_multi_model.py"]