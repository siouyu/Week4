from flask import *  # 米字號是 import 全部功能、理論上是輸入需要的功能名
from cryptography.fernet import Fernet

app = Flask(__name__) # 建立 application 物件。app 是變數名稱，可自行更換
app.secret_key="secret"
key = Fernet.generate_key()
f = Fernet(key)

# Home page
@app.route("/", methods=["GET","POST"]) 
def home(): 
    if request.cookies.get("username"):
        return redirect("/member")
    else:
        return render_template("home.html")

# Verification
@app.route("/signin", methods=["GET","POST"]) 
def signin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            return redirect("/error?message=請輸入帳號和密碼")
        elif username == "test" and password == "test":
            byteUsername = str.encode(username)
            cipher = f.encrypt(byteUsername)
            resp = make_response(redirect("/member"))
            resp.set_cookie("username", cipher)
            return resp
        else:
            return redirect("/error?message=帳號或密碼輸入錯誤")
    else:
        return render_template("home.html")

# 會員頁
@app.route("/member", methods=["GET","POST"])
def member():
    if request.cookies.get("username"):
        return render_template("member.html")
    else:
        return redirect(url_for("home"))

# 失敗頁面
@app.route("/error")
def error():
    message = request.args.get("message")
    return render_template("error.html", message = message)

# User state management
@app.route("/signout")
def signout():
    res = make_response(redirect("/"))
    res.delete_cookie("username")
    return res


if __name__ == "__main__":
    app.run(port=3000, debug = True)
    app.secret_key = "secret"
