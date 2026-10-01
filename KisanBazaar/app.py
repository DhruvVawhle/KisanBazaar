from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample data for produce
produce_list = []

@app.route('/')
def index():
    return render_template('index.html', produce=produce_list)

@app.route('/list_produce', methods=['GET', 'POST'])
def list_produce():
    if request.method == 'POST':
        item = request.form['item']
        price = request.form['price']
        produce_list.append({'item': item, 'price': price})
        return redirect(url_for('index'))
    return render_template('list_produce.html')

@app.route('/negotiate_price/<int:produce_id>', methods=['GET', 'POST'])
def negotiate_price(produce_id):
    if request.method == 'POST':
        # Logic for negotiating price
        new_price = request.form['new_price']
        produce_list[produce_id]['price'] = new_price
        return redirect(url_for('index'))
    return render_template('negotiate_price.html', produce=produce_list[produce_id])

if __name__ == '__main__':
    app.run(debug=True)
