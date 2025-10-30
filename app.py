from flask import Flask, render_template_string
import csv

app = Flask(__name__)

CSV_FILE = 'UM_C19_2021.csv'
PDF_CONTENT_FILE = 'pdf_content.txt'

def get_csv_data():
    with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
    return rows

def get_pdf_content():
    try:
        with open(PDF_CONTENT_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        # 将内容按页分割
        pages = []
        for page_section in content.split('--- 第 '):
            if page_section.strip():
                # 提取页码和内容
                parts = page_section.split(' 页 --')
                if len(parts) > 1:
                    page_num = parts[0].strip()
                    page_content = parts[1].strip()
                    pages.append({'number': page_num, 'content': page_content})
        return pages
    except Exception as e:
        print(f"读取PDF内容时出错: {str(e)}")
        return []

@app.route('/')
def index():
    # 默认显示PDF内容页面
    return render_template_string(
        '''
        <html>
        <head>
            <title>文档查看器</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; }
                .nav { background: #333; padding: 10px; margin-bottom: 30px; }
                .nav a { color: white; text-decoration: none; padding: 10px 20px; display: inline-block; }
                .nav a:hover { background: #555; }
                h1 { color: #333; }
            </style>
        </head>
        <body>
            <div class="nav">
                <a href="/pdf">PDF文档内容</a>
                <a href="/csv">CSV数据表格</a>
            </div>
            <h1 style="text-align:center;">欢迎使用文档查看器</h1>
            <p style="text-align:center;">请选择上方导航查看您的文档内容</p>
        </body>
        </html>
        '''
    )

@app.route('/csv')
def csv_view():
    rows = get_csv_data()
    headers = rows[0]
    data = rows[1:]
    return render_template_string(
        '''
        <html>
        <head>
            <title>CSV数据表格</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; }
                .nav { background: #333; padding: 10px; margin-bottom: 30px; }
                .nav a { color: white; text-decoration: none; padding: 10px 20px; display: inline-block; }
                .nav a:hover { background: #555; }
                table { border-collapse: collapse; width: 95%; margin: 30px auto; }
                th, td { border: 1px solid #aaa; padding: 8px 12px; }
                th { background-color: #f2f2f2; }
                tr:nth-child(even) { background: #f9f9f9; }
            </style>
        </head>
        <body>
            <div class="nav">
                <a href="/pdf">PDF文档内容</a>
                <a href="/csv">CSV数据表格</a>
            </div>
            <h2 style="text-align:center;">UM_C19_2021.csv 数据</h2>
            <table>
                <thead>
                    <tr>
                        {% for h in headers %}<th>{{ h }}</th>{% endfor %}
                    </tr>
                </thead>
                <tbody>
                    {% for row in data %}
                        <tr>
                            {% for item in row %}<td>{{ item }}</td>{% endfor %}
                        </tr>
                    {% endfor %}
                </tbody>
            </table>
        </body>
        </html>
        ''', headers=headers, data=data)

@app.route('/pdf')
def pdf_view():
    pages = get_pdf_content()
    return render_template_string(
        '''
        <html>
        <head>
            <title>PDF文档内容</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; }
                .nav { background: #333; padding: 10px; margin-bottom: 30px; }
                .nav a { color: white; text-decoration: none; padding: 10px 20px; display: inline-block; }
                .nav a:hover { background: #555; }
                .page { background: #f9f9f9; border: 1px solid #ddd; padding: 20px; margin-bottom: 30px; border-radius: 5px; }
                .page h3 { color: #333; border-bottom: 1px solid #ddd; padding-bottom: 10px; }
                pre { white-space: pre-wrap; word-wrap: break-word; }
            </style>
        </head>
        <body>
            <div class="nav">
                <a href="/pdf">PDF文档内容</a>
                <a href="/csv">CSV数据表格</a>
            </div>
            <h2 style="text-align:center;">YourFirstWebapp.pdf 内容</h2>
            {% if pages %}
                {% for page in pages %}
                    <div class="page">
                        <h3>第 {{ page.number }} 页</h3>
                        <pre>{{ page.content }}</pre>
                    </div>
                {% endfor %}
            {% else %}
                <p style="text-align:center; color: red;">无法加载PDF内容</p>
            {% endif %}
        </body>
        </html>
        ''', pages=pages)

if __name__ == '__main__':
    app.run(debug=True)
