import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

ITEMS = [
    {"id": 1, "name": "Gaming Laptop", "price": 100000, "icon": "💻"},
    {"id": 2, "name": "4K OLED TV", "price": 50000, "icon": "📺"},
    {"id": 3, "name": "Anime Girl Pillow", "price": 2500, "icon": "🛌"},
    {"id": 4, "name": "CTF Flag Solving Service", "price": 500, "icon": "🚩"}
]

@app.route('/')
def index():
    return render_template('index.html', items=ITEMS)

@app.route('/checkout', methods=['POST'])
def checkout():
    try:
        item_id = int(request.form.get('item_id', 0))
        price_paid = int(request.form.get('price', -1))
    except ValueError:
        return jsonify({"success": False, "message": "Invalid parameters structure."}), 400

    # Verify if buying the target flag item
    if item_id == 4:
        if price_paid == 0:
            # FIX: Fetch the flag dynamically right when the exploit succeeds!
            # If GZCTF_FLAG is missing, it will clearly tell you the Env Var is not set.
            actual_flag = os.environ.get('GZCTF_FLAG', 'Error: GZCTF_FLAG environment variable not found!')
            
            return jsonify({
                "success": True, 
                "exploit": True,
                "message": f"[+] Parameter Tampering Success! Flag: {actual_flag}"
            })
            
        elif price_paid >= 500:
            return jsonify({
                "success": True, 
                "exploit": False,
                "message": "Transaction successful! Thank you for the payment. Contact admin to claim your points manually."
            })
        else:
            return jsonify({"success": False, "message": "Insufficient funds! The price is 500."}), 400
            
    return jsonify({"success": False, "message": "Item out of stock or invalid."}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9994)
