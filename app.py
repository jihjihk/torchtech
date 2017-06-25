from flask import Flask, request, url_for, redirect, render_template
app = Flask(__name__)

@app.route('/')
def index():
    author = "Me"
    name = "Jihyun"
    return render_template('index.html', author=author, name=name)

@app.route('/elements', methods=['GET', 'POST'])
def urgent_btn():
	if request.method == 'POST':
		return redirect(url_for('index'))
	return render_template('urgent.html')

@app.route('/danger', methods=['GET', 'POST'])
def danger_btn():
	if request.method == 'POST':
		return redirect(url_for('index'))
	return render_template('danger.html')

@app.route('/safewalk', methods=['GET', 'POST'])
def safewalk_btn():
	if request.method == 'POST':
		return redirect(url_for('index'))
	return render_template('safewalk.html')


@app.route('/submit', methods=['GET', 'POST'])
def submit_btn():
	if request.method == 'POST':
		return redirect(url_for('index'))
	return render_template('urgent.html')

@app.route('/submit', methods=['GET', 'POST'])
def safe_submit_btn():
	if request.method == 'POST':
		return redirect(url_for('index'))
	return render_template('safewalk_res.html')








if __name__ == "__main__":
    app.run(debug=True)

