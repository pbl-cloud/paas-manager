from flask import Flask, render_template
 
app = Flask(__name__)
 
class Item:
    def __init__(item, name, filename, status):
	    item.name = name
	    item.filename = filename
	    item.status = status
 
@app.route("/")
def list():
    items = [Item( 'honda', 'aiueo.jar', 'waiting'), Item( 'kagawa', 'kakikukeko.jar', 'finished') ]
    return render_template("index.html", items=items)
	
@app.route("/hadoooop", methods=['GET', 'POST'])
def lista():
    items = [Item( 'honda', 'aiueo.jar', 'waiting'), Item( 'kagawa', 'kakikukeko.jar', 'finished') ]
    return render_template("index.html", items=items)
	
	
 
app.run()