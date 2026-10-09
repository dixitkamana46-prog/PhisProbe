from flask import Flask, render_template, request, jsonify
import re  #regular expresiion checks
import socket #find ip address

app = Flask(__name__) #start kregi web app

# Smart heuristic detection
def calculate_risk(url):
    score = 0
    reasons = []
    

    if len(url) > 75:
        score += 15
        reasons.append("URL too long")

    if not url.startswith("https"):
        score += 20
        reasons.append("Not using HTTPS")

    suspicious_words = ["login", "verify", "secure", "update", "bank", "free", "bonus", "money", "give", "free", "jackpot"]
    for word in suspicious_words:
        if word in url.lower():


            
            score += 10
            reasons.append(f"Contains '{word}'")

    if url.count("-") > 3:
        score += 10
        reasons.append("Too many hyphens")

    if "@" in url:
        score += 25
        reasons.append("@ symbol detected")

    if re.search(r"\d+\.\d+\.\d+\.\d+", url):
        score += 25
        reasons.append("Uses IP instead of domain")

    if url.count(".") > 3:
        score += 10
        reasons.append("Too many subdomains")

    return min(score, 100), reasons



#  Domain info
def get_domain_info(url):
    try:
        domain = url.split("//")[-1].split("/")[0]
        ip = socket.gethostbyname(domain)
        return {"domain": domain, "ip": ip}
    except:
        return {"domain": "Unknown", "ip": "Unknown"}


@app.route("/")
def home():
    return render_template("indexi.html")


@app.route("/scan", methods=["POST"])
def scan():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    risk_score, reasons = calculate_risk(url)
    domain_info = get_domain_info(url)

    return jsonify({
        "risk": risk_score,
        "reasons": reasons,
        "domain": domain_info["domain"],
        "ip": domain_info["ip"]
    })


if __name__ == "__main__":
    app.run(debug=True)