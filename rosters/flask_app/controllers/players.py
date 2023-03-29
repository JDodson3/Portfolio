from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.player import Player
from flask_app.models.user import User

@app.route('/dashboard')
def dashboard():
	if 'user_id' not in session:
		return redirect('/login')
	user = User.getOne({"id":session['user_id']})
	if not user:
		return redirect('/logout')
		
	return render_template('dashboard.html', user=user, players=Player.getAll())

@app.route('/addPlayer')
def addPlayer():
	if 'user_id' not in session:
		return redirect('/')
	user = User.getOne({"id":session['user_id']})
	return render_template('addPlayer.html', user=user)

@app.route('/createPlayer', methods=['POST'])
def createPlayer():
	if 'user_id' not in session:
		return redirect('/')
	if not Player.validate_player(request.form):
		return redirect('/addPlayer')
	data = {
		'first_name': request.form['first_name'],
		'last_name': request.form['last_name'],
		'height': request.form['height'],
		'weight': request.form['weight'],
		'grade': request.form['grade'],
		'points_game': request.form['points_game'],
		'rebounds_game': request.form['rebounds_game'],
		'assists_game': request.form['assists_game'],
		'blocks_game': request.form['blocks_game'],
		'steals_game': request.form['steals_game'],
		'bio': request.form['bio'],
		'user_id': session['user_id']
	}
	Player.save(data)
	return redirect('/dashboard')

@app.route('/players/<int:id>/view')
def viewPlayer(id):
	if 'user_id' not in session:
		return redirect('/')
	user = User.getOne({"id":session['user_id']})
	return render_template('viewPlayer.html', user=user, player=Player.getOne({'id':id}))

@app.route('/players/<int:id>/edit')
def editPlayer(id):
	if 'user_id' not in session:
		return redirect('/')
	user = User.getOne({"id":session['user_id']})
	return render_template('editPlayer.html', user=user, player=Player.getOne({'id':id}))

@app.route('/players/<int:id>/update', methods=['POST'])
def updatePlayer(id):
	if 'user_id' not in session:
		return redirect('/')
	if not Player.validate_player(request.form):
		return redirect(f'/players/{id}/edit')
	data = {
		'id': id,
		'first_name': request.form['first_name'],
		'last_name': request.form['last_name'],
		'height': request.form['height'],
		'weight': request.form['weight'],
		'grade': request.form['grade'],
		'points_game': request.form['points_game'],
		'rebounds_game': request.form['rebounds_game'],
		'assists_game': request.form['assists_game'],
		'blocks_game': request.form['blocks_game'],
		'steals_game': request.form['steals_game'],
		'bio': request.form['bio']
	}
	Player.update(data)
	return redirect('/dashboard')

@app.route('/players/<int:id>/delete')
def deletePlayer(id):
	if 'user_id' not in session:
		return redirect('/')
	Player.delete({'id':id})
	return redirect('/dashboard')
