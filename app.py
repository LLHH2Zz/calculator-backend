import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, jsonify

# 路径配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, '..', 'frontend')
DB_PATH = os.path.join(BASE_DIR, 'calculator.db')

# 初始化Flask，指定前端模板路径
app = Flask(
    __name__,
    template_folder=FRONTEND_DIR,
    static_folder=FRONTEND_DIR,
    static_url_path=''
)

# ---------------------- 数据库持久化 ----------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expression TEXT NOT NULL,
            result TEXT NOT NULL,
            time TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_record(expr, result, time_str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO history (expression, result, time) VALUES (?, ?, ?)',
        (expr, result, time_str)
    )
    conn.commit()
    conn.close()

def get_all_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT expression, result, time FROM history ORDER BY id DESC')
    records = cursor.fetchall()
    conn.close()
    return [{"expr": r[0], "result": r[1], "time": r[2]} for r in records]

def clear_all_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM history')
    conn.commit()
    conn.close()

# ---------------------- 接口路由 ----------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    expr = data.get("expression", "")
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    try:
        safe_expr = expr.replace("×", "*").replace("÷", "/")
        result = eval(safe_expr)

        # 除零判断
        if isinstance(result, float) and (result == float('inf') or result == float('-inf')):
            raise ZeroDivisionError

        # 整数结果去掉小数点
        res_str = str(int(result)) if isinstance(result, float) and result.is_integer() else str(result)

    except ZeroDivisionError:
        res_str = "错误：除以零"
    except Exception:
        res_str = "错误：无效表达式"

    add_record(expr, res_str, time_str)
    history = get_all_history()
    return jsonify({"record": {"expr": expr, "result": res_str, "time": time_str}, "history": history})

@app.route('/get_history', methods=['GET'])
def get_history():
    return jsonify({"history": get_all_history()})

@app.route('/clear_history', methods=['POST'])
def clear_history():
    clear_all_history()
    return jsonify({"msg": "历史已清空", "history": []})

if __name__ == '__main__':
    init_db()
    # 监听所有网卡，支持内网访问
    app.run(host="0.0.0.0", port=5000, debug=False)
