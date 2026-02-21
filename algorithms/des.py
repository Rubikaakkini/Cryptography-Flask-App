from flask import Flask, render_template, request

app = Flask(__name__)

S0 = [
    [1,0,3,2],
    [3,2,1,0],
    [0,2,1,3],
    [3,1,3,2]
]

S1 = [
    [0,1,2,3],
    [2,0,1,3],
    [3,0,1,0],
    [2,1,0,3]
]

def permute(bits, table):
    return ''.join(bits[i-1] for i in table)

def left_shift(bits, n):
    return bits[n:] + bits[:n]

def xor(a, b):
    return ''.join(str(int(x)^int(y)) for x,y in zip(a,b))

def bin2(n):
    return format(n, '02b')

def sbox(bits, box):
    row = int(bits[0] + bits[3], 2)
    col = int(bits[1] + bits[2], 2)
    return bin2(box[row][col])

@app.route('/', methods=['GET', 'POST'])
def index():
    output = ""
    if request.method == 'POST':

        pt = request.form['pt'].strip()
        key = request.form['key'].strip()

        P10 = list(map(int, request.form['p10'].split()))
        P8 = list(map(int, request.form['p8'].split()))
        IP = list(map(int, request.form['ip'].split()))
        IP_INV = list(map(int, request.form['ipinv'].split()))
        EP = list(map(int, request.form['ep'].split()))

        output += "STEP 1: KEY GENERATION\n"
        p10_key = permute(key, P10)
        output += f"P10(K) = {p10_key}\n"

        L, R = p10_key[:5], p10_key[5:]
        L = left_shift(L, 1)
        R = left_shift(R, 1)

        K1 = permute(L + R, P8)
        output += f"LS-1 → P8 → K1 = {K1}\n\n"

        output += "STEP 2: INITIAL PERMUTATION\n"
        ip = permute(pt, IP)
        L0, R0 = ip[:4], ip[4:]
        output += f"IP(PT) = {ip}\n"
        output += f"L0 = {L0}, R0 = {R0}\n\n"

        output += "STEP 3: FUNCTION F\n"
        ep = permute(R0, EP)
        output += f"EP(R0) = {ep}\n"

        x = xor(ep, K1)
        output += f"EP(R0) ⊕ K1 = {x}\n"

        s0_out = sbox(x[:4], S0)
        s1_out = sbox(x[4:], S1)

        output += f"S0 Output = {s0_out}\n"
        output += f"S1 Output = {s1_out}\n"

        F = s0_out + s1_out
        output += f"F = {F}\n\n"

        output += "STEP 4: XOR WITH L0\n"
        R1 = xor(L0, F)
        L1 = R0
        output += f"L1 = {L1}, R1 = {R1}\n\n"

        output += "STEP 5: IP INVERSE\n"
        cipher = permute(L1 + R1, IP_INV)
        output += f"Cipher Text = {cipher}"

    return render_template('DES.html', output=output)

if __name__ == '__main__':
    app.run(debug=True)
