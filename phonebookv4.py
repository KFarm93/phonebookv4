from flask import Flask, render_template, request, redirect
import pg

db = pg.DB(dbname='phonebook_db')
app = Flask('phonebook4')


@app.route('/')
def list_entries():
    query = db.query('select * from phonebook')

    return render_template(
        'list_all.html',
        title="Entry List",
        entry_list=query.namedresult())


@app.route('/new_entry')
def add_entry():
    return render_template(
        'new_entry.html',
        title="New Entry")

@app.route('/submit_new_entry', methods=['POST'])
def submit_new_entry():
    name = request.form.get('name')
    phone_number = request.form.get('phone_number')
    email = request.form.get('email')
    db.insert(
        'phonebook',
        name=name,
        phone_number=phone_number,
        email=email)
    return redirect('/')

@app.route('/update_entry')
def update_entry():
    id = int(request.args.get('id'))
    query = db.query('''
    select * from phonebook
    where id = %d''' % id)
    entry = query.namedresult()[0]
    return render_template(
        'update_entry.html',
        title="Update Entry",
        entry=entry)


@app.route('/submit_updated_entry', methods=['POST'])
def submit_updated_entry():
    id = int(request.form.get('id'))
    name = request.form.get('name')
    phone_number = request.form.get('phone_number')
    email = request.form.get('email')
    action = request.form.get('action')
    if action == 'update':
      db.update('phonebook', {
      'id': id,
      'name': name,
      'phone_number': phone_number,
      'email': email
      })
    elif action =='delete':
      db.delete('phonebook', {'id': id})
    else:
        raise Exception("Invalid action.")
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
