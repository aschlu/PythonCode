from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

# 假資料
data = [
    {"host": "H1", "db": "DB1", "type": "BACKUP", "status": "✅"},
    {"host": "H1", "db": "DB1", "type": "ALERT", "status": "❌"},
]

# 登入頁
@app.get("/", response_class=HTMLResponse)
def login_page():
    return """
    <h2>DB巡檢系統 DEMO</h2>
    <form action="/login" method="post">
        帳號: <input name="username"><br>
        密碼: <input name="password" type="password"><br>
        <button type="submit">登入</button>
    </form>
    """

# 登入處理
@app.post("/login", response_class=HTMLResponse)
def login(username: str = Form(...), password: str = Form(...)):
    return f"""
    <h3>歡迎 {username}</h3>
    <a href="/report">進入週報</a>
    """

# 週報頁
@app.get("/report", response_class=HTMLResponse)
def report():
    rows = ""
    for r in data:
        rows += f"""
        <tr>
            <td>{r['host']}</td>
            <td>{r['db']}</td>
            <td>{r['type']}</td>
            <td>{r['status']}</td>
        </tr>
        """

    return f"""
    <h2>週報</h2>
    <table border="1">
        <tr><th>HOST</th><th>DB</th><th>TYPE</th><th>狀態</th></tr>
        {rows}
    </table>
    <br>
    <a href="/process">填寫處理說明</a><br><br>
    <a href="/approve">簽核</a>
    """

# 處理說明
@app.get("/process", response_class=HTMLResponse)
def process_page():
    return """
    <h3>填寫處理說明</h3>
    <form action="/process" method="post">
        <textarea name="desc" rows="4" cols="50"></textarea><br>
        <button type="submit">送出</button>
    </form>
    """

@app.post("/process", response_class=HTMLResponse)
def process(desc: str = Form(...)):
    return f"""
    <h3>已儲存處理說明</h3>
    <p>{desc}</p>
    <a href="/report">回報表</a>
    """

# 簽核
@app.get("/approve", response_class=HTMLResponse)
def approve():
    return """
    <h2>簽核完成 ✅</h2>
    <a href="/report">回報表</a>
    """

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
