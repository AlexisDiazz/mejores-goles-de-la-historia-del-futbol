 document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('contact-form');

    form.addEventListener('submit', function(event) {
      event.preventDefault(); // Prevent default form submission

      // Reset previous errors
      resetErrors();

      // Get form values
      const name = document.getElementById('name').value.trim();
      const email = document.getElementById('email').value.trim();
      const message = document.getElementById('message').value.trim();

      // Basic validation
      let isValid = true;

      if (name === '') {
        showError('name', 'Por favor, introduce tu nombre.');
        isValid = false;
      }

      if (email === '') {
        showError('email', 'Por favor, introduce tu email.');
        isValid = false;
      } else if (!isValidEmail(email)) {
        showError('email', 'Por favor, introduce un email válido.');
        isValid = false;
      }

      if (message === '') {
        showError('message', 'Por favor, introduce un mensaje.');
        isValid = false;
      }

        // If client-side validation passes, send data to the backend
      if (isValid) {
            const formData = new FormData(form);

            fetch('http://127.0.0.1:5000/contact', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    // Handle HTTP errors (e.g., 500, 400)
                    return response.json().then(data => {
                        throw new Error(data.error || 'Error en la solicitud');
                    });
                }
                return response.json();
            })
            .then(data => {
                // Handle success response
                console.log('Success:', data);
                alert(data.message || '¡Formulario enviado con éxito!');
                form.reset(); // Clear the form
            })
            .catch(error => {
                // Handle errors (network errors, errors from the server)
                console.error('Error:', error);
                alert('Hubo un error al enviar el formulario: ' + error.message);
            });
      }
    });

    // Helper functions
    function isValidEmail(email) {
      // Basic email validation regex
      return /^[w-]+(.[w-]+)*@([w-]+.)+[a-zA-Z]{2,7}$/.test(email);
    }

    function showError(fieldId, errorMessage) {
      const field = document.getElementById(fieldId);
      field.classList.add('error'); // Add error class to the field

      let errorElement = field.nextElementSibling;
      if (!errorElement || !errorElement.classList.contains('error-message')) {
        errorElement = document.createElement('p');
        errorElement.classList.add('error-message');
        field.parentNode.insertBefore(errorElement, field.nextSibling);
      }
      errorElement.textContent = errorMessage;
    }

    function resetErrors() {
      const errorMessages = document.querySelectorAll('.error-message');
      errorMessages.forEach(function(error) {
        error.remove();
      });

      const errorFields = document.querySelectorAll('.error');
      errorFields.forEach(function(field) {
        field.classList.remove('error');
      });
    }
  });