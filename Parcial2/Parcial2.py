from flask import Flask, jsonify
import math

app = Flask(__name__)

@app.route('/numero/<int:num>')
def procesar_numero(num):
    factorial = math.factorial(num)

    if num % 2 == 0:
        etiqueta = "par"
    else:
        etiqueta = "impar"

    return jsonify({
        "numero": num,
        "factorial": factorial,
        "etiqueta": etiqueta
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)