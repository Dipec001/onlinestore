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

/* JS for contact html radio button */
document.addEventListener('DOMContentLoaded', function() {
  const contactRadio = document.getElementById('contact');
  const specialRequestRadio = document.getElementById('special-request');
  const contactForm = document.getElementById('contact-form');
  const contactQuestion = document.getElementById('contact-questions')
  const defaultFormHtml = contactForm.innerHTML;

  // Add event listener for radio button change
  contactRadio.addEventListener('change', function() {
      // Reset form to default
      contactForm.innerHTML = defaultFormHtml;
  });

  specialRequestRadio.addEventListener('change', function() {
      // Modify texts for special request
      contactQuestion.innerHTML = `
          <h2>Can’t Find The Product You’re Looking For On Our Website?</h2>
          <p>It is always a pleasure to hear from you. Kindly Fill In The Details Of What You Need, You will Get a Response As Soon As Possible</p>
      `;
      // Modify form for special request
      contactForm.innerHTML = `
          <!-- Special Request Form Fields -->
          <form action="{% url 'special_request' %}" method="POST" enctype="multipart/form-data">
              <!-- Special request form fields here -->
              <input type="text" name="name" placeholder="Name" required>
              <input type="text" name="phone_number" placeholder="Phone Number" required>
              <input type="email" name="email" placeholder="Email address" required>
              <input type="text" name="medicationName" placeholder="Name Of Medication " required>
              <textarea name="message" placeholder="What is the medication used for?" required></textarea>
              <input type="file" name="medicationImage" accept="image/*" style="border: none;" required>
              <button type="submit">Request Medication</button>
          </form>
      `;
  });
});


document.addEventListener('DOMContentLoaded', function() {
  const categories = document.getElementById('categories');
  const dropdownCat = document.querySelector('.cat-dropdown');

  function toggleDropdown() {
      const computedStyle = window.getComputedStyle(dropdownCat);
      if (computedStyle.display === 'none') {
          dropdownCat.style.display = 'block';
      } else {
          dropdownCat.style.display = 'none';
      }
  }

  categories.addEventListener('click', function(event) {
      event.stopPropagation();  // Prevent the click event from propagating to the document
      toggleDropdown();
  });

  // Close the dropdown when clicking outside of it
  document.body.addEventListener('click', function(event) {
      if (!event.target.closest('.category-title') && dropdownCat.style.display === 'block') {
          dropdownCat.style.display = 'none';
      }
  });
});
