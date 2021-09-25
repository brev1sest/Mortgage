from flask import Flask, jsonify, request, render_template,abort

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


@app.route('/banks/get_list', methods=['GET'])
def get_list():
    return jsonify(banks)

@app.route('/banks/add_bank', methods=['POST'])
def add_bank():
    new_one = request.json
    banks.append(new_one)
    return jsonify(banks)

@app.route('/banks/update_bank/<int:bank_id>', methods=['PUT'])
def update_bank(bank_id):
    item = next((x for x in banks if x['id'] == bank_id), None)
    params = request.json
    if not item:
        return {'message':'No banks with this id'}, 400
    item.update(params)
    return item


@app.route('/banks/delete_bank/<int:bank_id>', methods=['DELETE'])
def delete_bank(bank_id):
    idx = next((x for x in enumerate(banks)
                if x['id'] == bank_id), (None,None))
    banks.pop(idx) 
    return ''
    
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/banks/<int:bank_id>', methods=['CALCULATE'])
def calculate(bank_id):
        p = banks[bank_id]['maxium_loan']
        r = banks[bank_id]['interest_rate']
        n = banks[bank_id]['loan_term']
        t = r/12
        return p*t*((1+t)**n)/((1+t)**n - 1)

if __name__ == '__main__':
    app.run()
