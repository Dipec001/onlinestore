'use strict';

const optionsBox = document.querySelector('.options-box');

function toggleOptionsBox() {
  const computedStyle = window.getComputedStyle(optionsBox);

  if (computedStyle.display === 'none') {
    optionsBox.style.display = 'block'; // Show the options box
  } else {
    optionsBox.style.display = 'none'; // Hide the options box
  }
}

document.body.addEventListener('click', function(event) {
  console.log('Clicked on:', event.target);
  console.log('Options box display:', optionsBox.style.display);

  // Check if the clicked element is inside the .account div
  if (!event.target.closest('.account') && optionsBox.style.display === 'block') {
    console.log('Hiding options box');
    optionsBox.style.display = 'none'; // Hide the options box if clicked outside
  }
});



function togglePasswordVisibility() {
    const passwordInput = document.getElementById('password');
    const toggleIcon = document.querySelector('.toggle-password i');
    const showToggleIcon = document.querySelector('.toggle-password i.fa-eye');
    const hideToggleIcon = document.querySelector('.toggle-password i.fa-eye-slash');

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        // toggleIcon.classList.remove('fa-eye');
        // toggleIcon.classList.add('fa-eye-slash');
        showToggleIcon.style.display = "block";
        hideToggleIcon.style.display = "none";
    } else {
        passwordInput.type = 'password';
        // toggleIcon.classList.remove('fa-eye-slash');
        // toggleIcon.classList.add('fa-eye');
        showToggleIcon.style.display = "none";
        hideToggleIcon.style.display = "block";
    }
}

