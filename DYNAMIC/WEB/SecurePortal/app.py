import os
import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from flask import Flask, abort, make_response, redirect, render_template, request, url_for

app = Flask(__name__)

KEY_DIR = os.path.join(os.path.dirname(__file__), "keys")
with open(os.path.join(KEY_DIR, "private.pem"), "rb") as f:
    PRIVATE_KEY = f.read()
with open(os.path.join(KEY_DIR, "public.pem"), "rb") as f:
    PUBLIC_KEY = f.read()  # exposed publicly at /publickey

_pub_obj = load_pem_public_key(PUBLIC_KEY)
PUBLIC_KEY_DER = _pub_obj.public_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
)

FLAG = os.environ.get("GZCTF_FLAG")

def issue_token(username: str, role: str) -> str:
    payload = {"user": username, "role": role}
    return jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")


def verify_token(token: str) -> dict:
    header = jwt.get_unverified_header(token)
    alg = header.get("alg")
    if alg == "RS256":
        return jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])
    elif alg == "HS256":
        return jwt.decode(token, PUBLIC_KEY_DER, algorithms=["HS256"])
    raise jwt.InvalidAlgorithmError("unsupported algorithm")


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip() or "guest"
        token = issue_token(username, "user")
        resp = make_response(redirect(url_for("dashboard")))
        resp.set_cookie("token", token, httponly=False)
        return resp
    return render_template("login.html")


@app.route("/logout")
def logout():
    resp = make_response(redirect(url_for("login")))
    resp.delete_cookie("token")
    return resp


@app.route("/dashboard")
def dashboard():
    token = request.cookies.get("token")
    if not token:
        return redirect(url_for("login"))
    try:
        payload = verify_token(token)
    except Exception:
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=payload.get("user"), role=payload.get("role"))


@app.route("/admin")
def admin():
    token = request.cookies.get("token")
    if not token:
        return redirect(url_for("login"))
    try:
        payload = verify_token(token)
    except Exception:
        abort(403)
    if payload.get("role") != "admin":
        abort(403)
    return render_template("admin.html", flag=FLAG, user=payload.get("user"))


@app.route("/publickey")
def publickey():
    return PUBLIC_KEY, 200, {"Content-Type": "text/plain"}


@app.errorhandler(403)
def forbidden(e):
    return render_template("forbidden.html"), 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
