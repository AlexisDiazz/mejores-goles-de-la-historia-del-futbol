from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.environ.get('HOME'), 'contact_form_submissions.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
db = SQLAlchemy(app)
# Define the model
class ContactFormSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return f'<Submission {self.id}: {self.name} - {self.email}>'
@app.route('/')
def index():
    return "¡Hola, Flask! La aplicación está funcionando correctamente."

@app.route('/contact', methods=['POST'])
def receive_contact_data():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')       
        
        try:
            new_submission = ContactFormSubmission(name=name, email=email, message=message)
            db.session.add(new_submission)
            db.session.commit()
            print('New contact form submission saved to the database.')
        print('Received contact form data:')
        print(f'  Name: {name}')
        print(f'  Email: {email}')
        print(f'  Message: {message}')

        return jsonify({'message': 'Form submitted successfully!'}), 200
    else:
        return jsonify({'error': 'Method not allowed'}), 405

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)