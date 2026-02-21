from flask import Flask, render_template, request

app = Flask(__name__)

# ---------- PRIME CHECK ----------
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# ---------- PRIMITIVE ROOT WITH STEPS ----------
def primitive_root_with_steps(p):
    steps = []

    for g in range(2, p):
        values = set()
        step_line = f"g = {g} → "

        for i in range(1, p):
            val = pow(g, i, p)
            values.add(val)
            step_line += f"{g}^{i} mod {p} = {val}, "

        step_line += f"\nUnique values count = {len(values)}"
        steps.append(step_line)

        if len(values) == p - 1:
            return g, steps

    return None, steps

# ---------- EUCLIDEAN ALGORITHM WITH STEPS ----------
def gcd_with_steps(a, b):
    steps = []
    orig_a, orig_b = a, b
    while b != 0:
        steps.append(f"{a} = {b} × {a // b} + {a % b}")
        a, b = b, a % b
    steps.append(f"GCD({orig_a}, {orig_b}) = {a}")
    return a, steps

# ---------- MAIN ROUTE ----------
@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    steps = []

    if request.method == "POST":
        algo = request.form.get("algorithm")

        if algo == "primitive":
            p = request.form.get("prime")
            if not p:
                result = "❌ Input cannot be empty"
            else:
                p = int(p)
                if not is_prime(p):
                    result = "❌ Enter a valid PRIME number"
                else:
                    root, steps = primitive_root_with_steps(p)
                    result = f" Primitive Root of {p} is {root}"

        elif algo == "gcd":
            a = request.form.get("num1")
            b = request.form.get("num2")
            if not a or not b:
                result = "❌ Both numbers are required"
            else:
                a, b = int(a), int(b)
                gcd_val, steps = gcd_with_steps(a, b)
                result = f"GCD of {a} and {b} is {gcd_val}"

    return render_template("primitivegcd.html", result=result, steps=steps)

# ---------- RUN SERVER ----------
if __name__ == "__main__":
    app.run(debug=True)
