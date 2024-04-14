from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, send_file
from jinja2 import Environment, FileSystemLoader
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from data import login, password
import sqlite3, werkzeug, io, os, shutil

 
smtp_server = smtplib.SMTP("smtp.mail.ru", 587)
smtp_server.starttls()
smtp_server.login(login, password)

# work_email = "jeff.papkin@mail.ru"
# work_email = "mishamx04@gmail.com"
work_email = "dizastes@gmail.com"
savefilePath = "static/media/"


def updateCardsInformation(category):
	con = sqlite3.connect("bd.db")
	cursor = con.cursor()
	cards = []
	cursor.execute("select id, category, description, thing, title, src from cards where category = ? AND type = 'project'", (category,))
	cards = [{'id':row[0],'category': row[1], 'description': row[2], 'thing': row[3], 'title': row[4], 'src': row[5]} for row in cursor.fetchall()]
	return cards

def updateDeviceInformation(category):
	con = sqlite3.connect("bd.db")
	cursor = con.cursor()
	cards = []
	cursor.execute("select id, category, description, thing, title, src from cards where category = ? AND type = 'device'", (category,))
	cards = [{'id':row[0],'category': row[1], 'description': row[2], 'thing': row[3], 'title': row[4], 'src': row[5]} for row in cursor.fetchall()]
	return cards


app = Flask(__name__)

ALLOWED_EXTENSIONS = {'jpeg', 'jpg', 'png','gif'}
ALLOWED_EXTENSIONS_PRJ = ALLOWED_EXTENSIONS | {'mp4'}

def allowed_file(filename, _type):
	if(_type == 'device'):
		return '.' in filename and \
			filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	else:
		return '.' in filename and \
			filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_PRJ

app.secret_key = "k3jh54k2jhjl23j1j23"

def send_email(message, clien_email, work_email):
	msg = MIMEMultipart()	 
	msg["From"] = login
	msg["To"] = work_email
	msg["Subject"] = f"Сообщение от клиента {clien_email}"
	text = message
	msg.attach(MIMEText(text, "plain"))	 
	smtp_server.sendmail(login, work_email, msg.as_string())	 
	smtp_server.quit()

@app.route('/', methods=['post', "get"])
def home():
	if request.method == "GET":
		con = sqlite3.connect("bd.db")
		cursor = con.cursor()
		cards = updateCardsInformation('VR/AR/MR')
		devicesCard = updateDeviceInformation('VR/AR/MR')
		return render_template("index.html", cards = cards, devicesCard=devicesCard)
	elif request.method == "POST":
		email = request.form.get("email")
		text = request.form.get("text_area")
		send_email(text, email, work_email)
		return redirect(url_for("send"), 301)

@app.route("/send", methods=['post', "get"])
def send():
	return render_template("send.html")

@app.route("/change", methods=['POST', 'GET'])
def change():
	received_data = request.get_json()
	cards = updateCardsInformation(received_data['name'])
	deviceCards = updateDeviceInformation(received_data['name'])
	print(received_data['name'])
	return jsonify({'updatedCards': cards, 'updatedDeviceCards': deviceCards})

@app.route("/admin", methods=['post','get'])
def admin():
	admin_pass = "admin"
	flag = True

	con = sqlite3.connect("bd.db")
	cursor = con.cursor()
	cursor.execute("select id, category, description, thing, title, type from cards")
	arr = cursor.fetchall()
	arr = sorted(arr, key=lambda x: (x[1], x[5]), reverse=True)

	try:
		if session["login"] == True:
			flag = False
			return render_template("admin.html", flag=flag, arr=arr)
	except:
		if request.method == "POST":
			password = request.form["pass"]
			if password==admin_pass:
				flag = False
				session.permanent = True
				session["login"] = True
				return render_template("admin.html", flag=flag, arr=arr)
			else:
				return render_template("admin.html", flag=flag)
		elif request.method == "GET":
			flag = True
			return render_template("admin.html", flag=flag)


# @app.route("/admin/delete/<string:database>/<int:item_id>" , methods=['post', 'get'])
# def delete_item(item_id, database):
# 	con = sqlite3.connect("bd.db")
# 	cursor = con.cursor()
# 	cursor.execute(f"select url, project_id from gallery where id={item_id}")
# 	arr = cursor.fetchall()
# 	id_project = arr[0][1]
# 	if(os.path.exists(arr[0][0])):
# 		os.remove(arr[0][0])
# 	cursor.execute(f"delete from gallery where id={item_id}")
# 	con.commit()
# 	return redirect(url_for('change_data',id = id_project))

# @app.route("/admin/change", methods=['post' , 'get'])
# def change_data():
# 	if request.method =="GET":
# 		item_id = request.args.get('id')
# 	else:
# 		item_id = request.form['id']
# 	error=""
# 	con = sqlite3.connect("bd.db")
# 	cursor = con.cursor()
# 	cursor.execute(f"select category, description, thing, title, src, type, full_description from cards where id={item_id}")
# 	arr = cursor.fetchall()
# 	cards = []
# 	gallery = []
# 	equipment = []
# 	members = []
# 	cards.append({'category': arr[0][0], 'description': arr[0][1], 'thing': arr[0][2], 'title': arr[0][3], 'src': arr[0][4], 'type': arr[0][5], 'full_description': arr[0][6]})
# 	cursor.execute(f"select id, url from gallery where project_id={item_id}")
# 	arr = cursor.fetchall()
# 	for i in range(len(arr)):
# 		gallery.append({'id': arr[i][0], 'url': arr[i][1], 'database': 'gallery'})
# 	cursor.execute(f"select id, photo, title, description from equipment where project_id={item_id}")
# 	arr = cursor.fetchall()
# 	for i in range(len(arr)):
# 		equipment.append({'id': arr[i][0], 'photo': (arr[i][1]), 'title': arr[i][2], 'description': arr[i][3] ,'database': 'equipment'})
# 	cursor.execute(f"select id, photo, name, description from members where project_id={item_id}")
# 	arr = cursor.fetchall()
# 	for i in range(len(arr)):
# 		members.append({'id': arr[i][0], 'photo': arr[i][1], 'name': arr[i][2], 'description': arr[i][3] , 'database': 'members'})
# 	return render_template("change.html", arr=cards, id=item_id, error=error, type=cards[0]['type'], gallery=gallery, equipment=equipment, members=members)

@app.route("/AddProject", methods=['post','get'])
def AddProject():
	return render_template("add.html")

# @app.route("/update", methods=['post'])
# def update():
# 	con = sqlite3.connect("bd.db")
# 	cursor = con.cursor()
# 	item_id = request.form["id"]
# 	category = request.form["category"]
# 	description = request.form["description"]
# 	thing = request.form["thing"]
# 	title = request.form["title"]
# 	src = request.files["src"]
# 	_type = cursor.execute("select type from cards where id = ?", (item_id,)).fetchone()[0]
# 	if src and allowed_file(src.filename, _type):
# 		cursor.execute("select src from cards where id = ?", (item_id,))
# 		row = cursor.fetchone()  
# 		filepath = os.path.join(os.getcwd(), row[0]) 
# 		if(os.path.exists(filepath)):{
# 		os.remove(filepath)	
# 		}
# 		src.save(savefilePath+thing+src.filename)
# 		src = savefilePath+thing+src.filename
# 		cursor.execute("update cards set category=?, description=?, thing=?, title=?, src=? where id = ?", (category, description, thing, title, src, item_id))
# 		con.commit()
# 		return redirect("/admin")
# 	elif src and not allowed_file(src.filename, _type):
# 		return redirect(url_for('change_data', id=item_id))
# 	else: 
# 		cursor.execute("update cards set category=?, description=?, thing=?, title=? where id = ?", (category, description, thing, title, item_id))
# 		con.commit()
# 		return redirect("/admin")

@app.route("/delete", methods=['post'])
def delete():
	item_id = request.form["id"]
	con = sqlite3.connect("bd.db")
	cursor = con.cursor()
	cursor.execute("select src from cards where id = ?", (item_id,))
	row = cursor.fetchone()  
	filepath = os.path.join(os.getcwd(), row[0])
	filepath = os.path.dirname(filepath)
	if(os.path.exists(filepath)):
		shutil.rmtree(filepath, ignore_errors=True)
	cursor.execute(f"delete from cards where id = {item_id}")
	con.commit()
	return redirect("/admin")

@app.route("/add", methods=['post'])
def add():
	category = request.form["category"]
	description = request.form["description"]
	thing = request.form["thing"]
	title = request.form["title"]
	src = request.files["src"]
	_type = request.form["type"]
	full_description = request.form["full_description"]
	gallery = request.files.getlist("gallery[]")
	equipmentPhoto = request.files.getlist("equipmentPhoto[]")
	equipmentTitle = request.form.getlist("equipmentTitle[]")
	equipmentDescription = request.form.getlist("equipmentDescription[]")
	membersPhoto = request.files.getlist("membersPhoto[]")
	membersName = request.form.getlist("membersName[]")
	print(equipmentTitle)
	print(gallery)
	print(membersName)
	membersDescription = request.form.getlist("membersDescription[]")
	con = sqlite3.connect("bd.db")
	cursor = con.cursor()
	if src:
		category = category.replace('/', '_')
		if(not os.path.exists(savefilePath+category)):
			os.mkdir(savefilePath+category)
		if(_type == 'project'):
			filepath=os.path.join('static', 'media', category,title)
		else:
			filepath=os.path.join('static', 'media', category, _type)
		if(not os.path.exists(filepath)):
			os.mkdir(filepath)
		src.save(os.path.join(filepath, src.filename))
		src = os.path.join(filepath, src.filename).replace('\\', '/')
		cursor.execute("INSERT INTO cards (category, description, thing, title, src, type, full_description) VALUES (?, ?, ?, ?, ?, ?,?)", (category.replace('_','/'), description, thing, title, src, _type, full_description))
		con.commit()
		if(_type == 'project'):
			thisID = cursor.lastrowid
			if (not os.path.exists(filepath+'\\gallery') and gallery != ['']):
				os.mkdir(filepath+'\\gallery')
				for i in range(len(gallery)):
					photopath = os.path.join(filepath+'\\gallery', gallery[i].filename)
					gallery[i].save(photopath)
					cursor.execute("INSERT INTO gallery (project_id, url) VALUES (?, ?)", (thisID, photopath.replace('\\', '/')))
					con.commit()
			if (not os.path.exists(filepath+'\\equipment') and equipmentTitle != ['']):
				os.mkdir(filepath+'\\equipment')
				for i in range(len(equipmentTitle)):
					photopath = os.path.join(filepath+'\\equipment', equipmentPhoto[i].filename)
					equipmentPhoto[i].save(photopath)
					cursor.execute("INSERT INTO equipment (project_id, photo, title, description) VALUES (?, ?, ?,?)", (thisID, photopath.replace('\\', '/'), equipmentTitle[i], equipmentDescription[i]))
					con.commit()
			if (not os.path.exists(filepath+'\\members') and membersName != ['']):
				os.mkdir(filepath+'\\members')
				for i in range(len(membersName)):
					photopath = os.path.join(filepath+'\\members', membersPhoto[i].filename)
					membersPhoto[i].save(photopath)
					cursor.execute("INSERT INTO members (project_id, photo, name, description) VALUES (?, ?, ?, ?)", (thisID, photopath.replace('\\', '/'), membersName[i], membersDescription[i]))
					con.commit()
		return redirect("/admin")
	else:
		return redirect("/admin")

@app.route("/information/<int:card_id>", methods=['post', 'get'])
def information(card_id):
	con = sqlite3.connect("bd.db")
	cursor = con.cursor()
	cursor.execute(f"select category, description, thing, title, src, full_description from cards where id={card_id}")
	arr = cursor.fetchall()
	cards = []
	gallery = []
	equipment = []
	members = []
	cards.append({'category': arr[0][0], 'description': arr[0][1], 'thing': arr[0][2], 'title': arr[0][3], 'src': arr[0][4],'full_description': arr[0][5]})
	cursor.execute(f"select url from gallery where project_id={card_id}")
	arr = cursor.fetchall()
	for i in range(len(arr)):
		gallery.append(arr[i][0])
	cursor.execute(f"select photo, title, description from equipment where project_id={card_id}")
	arr = cursor.fetchall()
	for i in range(len(arr)):
		equipment.append({'photo': (arr[i][0]), 'title': arr[i][1], 'description': arr[i][2]})
	cursor.execute(f"select photo, name, description from members where project_id={card_id}")
	arr = cursor.fetchall()
	for i in range(len(arr)):
		members.append({'photo': arr[i][0], 'name': arr[i][1], 'description': arr[i][2]})
	return render_template("information.html", maininfo=cards, gallery=gallery, equipment = equipment, members = members)

@app.route("/logout", methods=['get','post'])
def logout():
	session.pop("login",None)
	session.clear()
	return redirect("/admin")

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')