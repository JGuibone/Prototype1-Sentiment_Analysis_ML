// Get the form element
const form = document.querySelector('form');

// Add a submit event listener to the form
form.addEventListener('submit', function(event) {
  // Prevent the form from submitting
  event.preventDefault();

  // Get the input elements within the form
  const inputs = form.querySelectorAll('input');

  // Flag to track if the form is valid
  let isValid = true;

  // Check if any of the input fields are empty
  inputs.forEach(function(input) {
    if (input.value.trim() === '') {
      // Input field is empty, mark form as invalid
      isValid = false;

      // Optionally, you can add custom error handling here, such as displaying an error message
      // Example: input.classList.add('error');
    }
  });

  // If the form is valid, submit it
  if (isValid) {
    form.submit();
  }
});
