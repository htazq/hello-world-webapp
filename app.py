import requests
from flask import Flask, render_template_string, request
# 导入 requests 可能产生的异常类型，用于更精细的错误处理
from requests.exceptions import RequestException, MissingSchema, InvalidURL

app = Flask(__name__)

# 更新后的 HTML 模板，包含输入、结果和错误显示
HTML_TEMPLATE = """
<!doctype html>
<html lang="zh">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>URL HTML 内容获取器</title> {# 修改标题 #}
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            padding-top: 2rem; /* 给顶部一些空间 */
            padding-bottom: 2rem;
            background-color: #f8f9fa;
        }
        .container {
            max-width: 800px; /* 限制内容最大宽度 */
        }
        .result-box {
            margin-top: 2rem;
            padding: 1.5rem;
            background-color: #e9ecef;
            border-radius: 0.3rem;
            /* 让内容可以滚动 */
            max-height: 60vh;
            overflow-y: auto;
            white-space: pre-wrap; /* 保留空白符并自动换行 */
            word-wrap: break-word;
            font-family: monospace; /* 使用等宽字体显示代码 */
            font-size: 0.85em; /* 稍小字体 */
            border: 1px solid #ced4da;
        }
        .error-message {
            color: #dc3545; /* 红色显示错误 */
            font-weight: bold;
            margin-top: 1rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="mb-4 text-center">URL HTML 内容获取器</h1>

        {# 输入表单 #}
        <form method="post">
            <div class="input-group mb-3">
                <span class="input-group-text">输入 URL:</span>
                <input type="text" class="form-control" id="urlInput" name="url_input" placeholder="必须包含 http:// 或 https://" required value="{{ original_url or '' }}">
                <button type="submit" class="btn btn-primary">获取 HTML</button>
            </div>
        </form>

        {# 显示错误信息 #}
        {% if error_message %}
        <div class="alert alert-danger" role="alert">
            <strong>出错了:</strong> {{ error_message }}
        </div>
        {% endif %}

        {# 显示获取到的 HTML 内容 #}
        {% if html_content is not none %} {# 检查 html_content 是否存在 (即使是空字符串也显示) #}
        <div class="result-area">
            <hr>
            <p><strong>从 {{ original_url }} 获取到的 HTML 内容:</strong></p>
            {# 使用 <pre> 或 <textarea> 来显示 HTML 源码比较合适 #}
            {# 使用 textarea 可以方便复制，且默认不会执行脚本 #}
            <textarea class="form-control result-box" rows="15" readonly>{{ html_content }}</textarea>
            {# 或者使用 pre 标签
            <pre class="result-box"><code>{{ html_content }}</code></pre>
            #}
        </div>
        {% elif not error_message %} {# 如果没有内容也没有错误，显示初始提示 #}
          <p class="text-center text-muted mt-4">输入一个网址来抓取它的 HTML 源代码吧！</p>
        {% endif %}

    </div>
</body>
</html>
"""

# 路由处理 GET 和 POST
@app.route('/', methods=['GET', 'POST'])
def index():
    """
    处理根路径请求。
    GET: 显示输入表单。
    POST: 获取用户输入的 URL，尝试抓取其 HTML 内容并显示。
    """
    original_url = ""
    html_content = None # 使用 None 作为初始状态，区分空字符串和未获取
    error_message = ""

    if request.method == 'POST':
        original_url = request.form.get('url_input', '').strip() # 去除首尾空格

        if not original_url:
            error_message = "请输入一个 URL。"
        # 基本检查，确保有 http:// 或 https://
        elif not original_url.lower().startswith(('http://', 'https://')):
             error_message = "URL 必须以 http:// 或 https:// 开头。"
        else:
            try:
                # 发送 GET 请求，设置超时，添加简单的 User-Agent
                # stream=True 可以用于大文件，但这里获取 text 通常还好
                # allow_redirects=True 是默认行为
                headers = {'User-Agent': 'MySimpleHTMLFetcher/1.0 (+http://example.com)'} # 礼貌性地设置 User-Agent
                response = requests.get(original_url, timeout=10, headers=headers)

                # 检查请求是否成功 (状态码 2xx)
                response.raise_for_status() # 如果状态码不是 2xx，会抛出 HTTPError

                # 获取响应内容的文本形式 (requests 会尝试猜测编码)
                # 注意：对于复杂的网站或非标准编码，这里可能需要更复杂的编码处理
                html_content = response.text

            # 捕获特定和通用的请求异常
            except MissingSchema:
                error_message = "URL 格式无效，缺少 'http://' 或 'https://'。"
            except InvalidURL:
                error_message = f"无法解析提供的 URL: '{original_url}'"
            except RequestException as e:
                # 捕获所有 requests 可能的异常，如连接错误、超时、重定向过多等
                error_message = f"请求 URL 时出错: {e}"
            except Exception as e:
                # 捕获其他意外错误
                error_message = f"发生未知错误: {e}"

    # 渲染模板，传递所有需要的数据
    return render_template_string(HTML_TEMPLATE,
                                  original_url=original_url,
                                  html_content=html_content,
                                  error_message=error_message)

if __name__ == '__main__':
    # 监听所有接口的 5000 端口
    # Gunicorn 会负责运行这个应用，但直接运行 python app.py 也能工作
    app.run(host='0.0.0.0', port=5000, debug=False) # 生产环境或部署时建议 debug=False