from flask import Flask, render_template_string

app = Flask(__name__)

# 简单的 HTML 模板
HTML_TEMPLATE = """
<!doctype html>
<html lang="zh">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Hello World 应用</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background-color: #f8f9fa;
        }
        .hello-box {
            padding: 3rem;
            background-color: #ffffff;
            border-radius: 0.5rem;
            box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="hello-box">
        <h1 class="display-4">{{ message }}</h1>
        <p class="lead">这是一个简单的 Flask Demo 应用。</p>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    """
    处理根路径的 GET 请求，返回 Hello World 页面。
    """
    hello_message = "Hello World!"
    # 渲染 HTML 模板，并传递消息
    return render_template_string(HTML_TEMPLATE, message=hello_message)

if __name__ == '__main__':
    # 在容器中运行时，监听所有接口的 5000 端口
    # Use host='0.0.0.0' to make the server accessible externally within the container network.
    # The port 5000 is exposed in the Dockerfile.
    app.run(host='0.0.0.0', port=5000)
