from flask import Flask, jsonify, request

app = Flask(__name__)

banks = [
    {
        'id' : 0,
        'name' : 'Test Bank',
        'interest_rate' : 10.00,
        'maximum_loan' : 100000,
        'minimum_down_payment' : 20.00,
        'loan_term' : 12,
    }
]


@app.route('/banks', methods=['GET'])
def get_list():
    return jsonify(banks)

@app.route('/banks', methods=['POST'])
def update_list():
    new_one = request.json
    new_one['id'] = banks[-1]['id'] + 1
    banks.append(new_one)
    return jsonify(banks)

@app.route('/banks/<int:bank_id>', methods=['PUT'])
def update_bank(bank_id):
    item = next((x for x in banks if x['id'] == bank_id), None)
    params = request.json
    if not item:
        return {'message':'No banks with this id'}, 400
    item.update(params)
    return item


@app.route('/banks/<int:bank_id>', methods=['DELETE'])
def delete_bank(bank_id):
    idx = next((x for x in enumerate(banks)
                 if x[1]['id'] == bank_id), (None,None))
    banks.pop(idx)
    return '',204
    
@app.route('/')
def index():
    return render_template('index.html')

def calculate(bank_id):
        p = banks[bank_id]['maxium_loan']
        r = banks[bank_id]['interest_rate']
        n = banks[bank_id]['loan_term']
        t = r/12
        return p*t*((1+t)**n)/((1+t)**n - 1)

if __name__ == '__main__':
    app.run()
