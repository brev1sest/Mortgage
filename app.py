from flask import Flask, jsonify, request, render_template
import pysqlite3

db = sqlite.connect('server.db')
sql = db.cursor()
app = Flask(__name__)

sql.execute( """
CREATE TABLE IF NOT EXISTS banks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    interest_rate INTEGER,
    maximum_loan INTEGER,
    minimum_down_payment INTEGER,
    loan_term INTEGER
)
""")
db.commit()



@app.route('/banks/get_list', methods=['GET'])
def get_list():
    sql.execute("SELECT * from banks")
    db.commit()
    db_banks = sql.fetchall()
    banks = []
    keys = ['id', 'name', 'interest_rate', 'maximum_loan', 'minimum_down_payment', 'loan_term']
    for val in db_banks:
        bank = {}
        for i in range(len(val)):
            bank[keys[i]] = val[i]
        banks.append(bank)
    return jsonify(banks)

@app.route('/banks/add_bank', methods=['POST'])
def add_bank():
    print(request.json)
    sql.execute(f"""
    INSERT INTO 
        banks (name, interest_rate, maximum_loan, minimum_down_payment, loan_term)
    VALUES
    ('{request.json['name']}', {request.json['interest_rate']}, {request.json['maximum_loan']}, {request.json['minimum_down_payment']}, {request.json['loan_term']})
    """)
    db.commit()
    return "done"

@app.route('/banks/update_bank/<int:bank_id>', methods=['PUT'])
def update_bank(bank_id):
    sql.execute(f"""
    UPDATE
        banks
    SET
        name = "{request.json['name']}",
        interest_rate = {request.json['interest_rate']},
        minimum_down_payment = {request.json['minimum_down_payment']},
        loan_term = {request.json['loan_term']}
    WHERE
        id = {bank_id}
    """)
    db.commit()
    return "done"


@app.route('/banks/delete_bank/<int:bank_id>', methods=['DELETE'])
def delete_bank(bank_id):
    sql.execute(f"DELETE from banks WHERE id = {bank_id}")
    db.commit()
    return "done"
    
    
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
