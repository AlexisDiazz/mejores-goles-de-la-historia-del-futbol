from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Configuración de la base de datos con una ruta absoluta
db_path = os.path.join(app.root_path, 'contact_form_submissions.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class ContactFormSubmission(db.Model):
    """
    Modelo para almacenar las sumisiones del formulario de contacto.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Submission {self.id}: {self.name} - {self.email}>'

@app.route('/')
def index():
    """
    Sirve la página de inicio enviando index.html desde la carpeta 'landing'.
    """
    return send_from_directory(os.path.join(app.root_path, 'landing'), 'index.html')


@app.route('/<path:filename>')
def serve_static(filename):
    """
    Sirve los archivos estaticos desde la ruta raiz
    """
    return send_from_directory(os.path.join(app.root_path), filename)

@app.route('/explicacion_goles/<path:filename>')
def serve_explicacion(filename):
    """
    Sirve los archivos desde la carpeta 'explicacion_goles'.
    """
    return send_from_directory(os.path.join(app.root_path, 'explicacion_goles'), filename)

@app.route('/contact', methods=['POST'])
def receive_contact_data():
    """
    Recibe, valida y guarda los datos enviados desde el formulario de contacto.
    """
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    # Validación básica
    if not (name and email and message):
        return jsonify({'error': 'Todos los campos son obligatorios.'}), 400

    try:
        new_submission = ContactFormSubmission(name=name, email=email, message=message)
        db.session.add(new_submission)
        db.session.commit()
        print('Nueva sumisión guardada.')
        return jsonify({'message': 'Formulario enviado exitosamente!'}), 200
    except Exception as e:
        db.session.rollback()
        print(f'Error: {e}')
        return jsonify({'error': 'Error guardando los datos.'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False)
