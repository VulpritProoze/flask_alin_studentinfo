from flask import Flask, render_template, redirect, request, flash, session
from flask_session import Session
import dbhelper
import os

app = Flask(__name__)
uploadfolder = 'static/img/'
app.config['SECRET_KEY'] = '!@#@$%@#@'
app.config['UPLOAD_FOLDER'] = uploadfolder
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

def get_users() -> object:
	table:str = 'users'
	return dbhelper.getall_record(table)

def get_students() -> object:
	table:str = 'students'
	return dbhelper.getall_record(table)

def getone_student(idno:str) -> object:
	table:str = 'students'
	return dbhelper.getone_record(table, idno=idno)

@app.route('/update_student', methods=['POST'])
def update_student():
	idno:str = request.form['idno']
	lastname:str = request.form['lastname']
	firstname:str = request.form['firstname']
	course:str = request.form['course']
	level:str = request.form['level']
	try:
		file:object = request.files['uploadimage']
		filename, extension = os.path.splitext(file.filename)
		imagename:str = os.path.join(uploadfolder, f'{filename}{idno}{extension}')
		files:list = [os.path.join(uploadfolder, f) for f in os.listdir(uploadfolder)]
		# os.path.join(uploadfolder, idno) checks for instance of when request.files fails to give the image file
		print('Update Student File: ', imagename)
		print('Update Student: ', files)
		if imagename != os.path.join(uploadfolder, idno):
			ok:bool = dbhelper.update_record('students', idno=idno, lastname=lastname, firstname=firstname, course=course, level=level, image=imagename)
			# If image is still the same image, then don't save the image
			if imagename not in files:
				file.save(imagename)
		else:
			ok:bool = dbhelper.update_record('students', idno=idno, lastname=lastname, firstname=firstname, course=course, level=level)
		flash('Update Student: Student updated successfully!') if ok else flash('Update Student: Student failed to update.')
	except:
		flash('Update Student: Student failed to update due to image error.')
	return redirect('/studentinfo')

@app.route('/delete_student', methods=['POST'])
def delete_student():
	idno:str = request.form['delete-student-input']
	image:str = getone_student(idno=idno)[0]['image']
	ok:bool = dbhelper.delete_record('students', idno=idno)
	flash('Delete Student: Student deleted successfully!') if ok else flash('Delete Student: Student failed to delete.')
	try:	
		os.remove(os.path.join(uploadfolder, image))
	except:
		flash('Delete Student: Image to be deleted does not exist.')
	return redirect('/studentinfo')

@app.route('/add_student', methods=['POST'])
def add_student():
	idno:str = request.form['idno']
	lastname:str = request.form['lastname']
	firstname:str = request.form['firstname']
	course:str = request.form['course']
	level:str = request.form['level']
	try:
		file:object = request.files['uploadimage']
		filename, extension = os.path.splitext(file.filename)
		imagename:str = os.path.join(uploadfolder, f'{filename}{idno}{extension}')
		ok:bool = dbhelper.add_record('students',idno=idno, lastname=lastname, firstname=firstname, course=course, level=level, image=imagename)
		if ok:
			file.save(imagename)
			flash('Add Student: Student added successfully!') if ok else flash('Add Student: Student failed to add.')
	except:
		flash('Add Student: Student failed to add due to an image error.')
	return redirect('/studentinfo')

@app.route('/studentinfo')
def studentinfo():
	if not session.get('name'):
		print('Log-in failed.')
		return redirect('/')
	else:	
		students=get_students()
		for student in students:
			print(student['image'])
		print('Log-in success!')
		return render_template('studentinfo.html', students=students, header=True)

@app.route('/logout')
def logout():
	session['name'] = None
	return redirect('/')

@app.route('/login', methods=['POST', 'GET'])
def login():
	users:object = get_users()
	usernames:list = [user['username'] for user in users]
	passwords:list = [user['password'] for user in users]
	login_username:str = request.form['username']
	login_password:str = request.form['password']
	for i in range(len(usernames)):
		if login_username == usernames[i] and login_password == passwords[i]:
			session['name'] = login_username
			return redirect('/studentinfo')
		else: 
			return redirect('/')

@app.after_request
def after_request(response):
	response.headers['Cache-Control'] = 'no cache, no-store, must-revalidate'
	return response

@app.route('/')
def index():
	return render_template('index.html', header=False) 

if __name__ == '__main__':
	app.run(debug=True)
