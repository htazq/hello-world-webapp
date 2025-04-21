from flask import Flask, render_template_string, request

app = Flask(__name__)

# 修改后的 HTML 模板，包含输入表单和结果显示区域
HTML_TEMPLATE = """
<!doctype html>
<html lang="zh">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>URL 反转器</title> {# 修改标题 #}
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background-color: #f8f9fa;
        }
        .content-box { {# 重命名 class 更通用 #}
            padding: 3rem;
            background-color: #ffffff;
            border-radius: 0.5rem;
            box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
            text-align: center;
            min-width: 400px; /* 给盒子一个最小宽度 */
        }
        .result {
            margin-top: 2rem; /* 结果区域与表单的间距 */
            word-wrap: break-word; /* 长字符串自动换行 */
        }
        .reversed-url {
             color: #dc3545; /* 红色突出显示 */
             font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="content-box">
        <h1 class="display-5 mb-4">URL 反转器</h1> {# 修改主标题 #}

        {# 添加输入表单 #}
        <form method="post">
            <div class="mb-3">
                <label for="urlInput" class="form-label">输入一个 URL:</label>
                <input type="text" class="form-control" id="urlInput" name="url_input" placeholder="例如：https://www.example.com/path?query=1" required value="{{ original_url or '' }}"> {# 保留上次输入 #}
            </div>
            <button type="submit" class="btn btn-primary">反转它！</button>
        </form>

        {# 添加结果显示区域，仅当有结果时显示 #}
        {% if reversed_url %}
        <div class="result">
            <hr> {# 分隔线 #}
            <p><strong>原始 URL:</strong><br> {{ original_url }}</p>
            <p><strong>反转之后:</strong><br> <span class="reversed-url">{{ reversed_url }}</span></p>
        </div>
        {% else %}
         <p class="lead mt-4">输入一个网址，看看反转后是什么搞笑的样子！</p> {# 初始提示语 #}
        {% endif %}

    </div>
</body>
</html>
"""

# 修改路由以处理 GET 和 POST 请求
@app.route('/', methods=['GET', 'POST'])
def index():
    """
    处理根路径的 GET 和 POST 请求。
    GET: 显示输入表单。
    POST: 获取输入的 URL，反转它，并显示结果。
    """
    original_url = ""
    reversed_url = ""

    if request.method == 'POST':
        # 从表单获取用户输入的 URL，使用 .get 提供默认值以防万一
        original_url = request.form.get('url_input', '')
        if original_url:
            # 使用 Python 的切片功能反转字符串
            reversed_url = original_url[::-1]

    # 渲染 HTML 模板，并传递原始 URL 和反转后的 URL
    # 如果是 GET 请求或 POST 请求但无输入，reversed_url 会是空字符串，模板中的结果区域不显示
    return render_template_string(HTML_TEMPLATE, original_url=original_url, reversed_url=reversed_url)

if __name__ == '__main__':
    # 监听所有接口的 5000 端口
    app.run(host='0.0.0.0', port=5000)