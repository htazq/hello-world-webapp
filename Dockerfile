# 使用官方 Python 基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
# --no-cache-dir: 不存储缓存，减小镜像体积
# --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org: 为了处理可能的网络问题，显式信任 Pypi 源
RUN pip install --no-cache-dir --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org -r requirements.txt

# 复制应用代码到工作目录
COPY app.py .

# 暴露 Flask 应用运行的端口
EXPOSE 5000

# 设置容器启动时执行的命令
CMD ["python", "app.py"]
