from flask import Flask, render_template, request
from werkzeug import secure_filename
 
app = Flask(__name__)
 
class Item:
    def __init__(item, name, filename, status):
	    item.name = name
	    item.filename = filename
	    item.status = status
 

items = []

@app.route("/")
def view_index():
    return render_template("index.html", items=items)
	
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['jarfile']
        f.save('/tmp/uploads/' + secure_filename(f.filename))
        items.append( Item(request.form['username'], f.filename, 'waiting') )
    return render_template("index.html", items=items)
    
if __name__ == '__main__':
    app.run(debug=True)
