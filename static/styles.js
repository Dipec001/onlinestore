'use strict';

// Testing purpose
console.log('JavaScript file loaded successfully');

function testFunction() {
    console.log('Window resized');
}

window.addEventListener('resize', function() {
    testFunction();
});
// testing purpose


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

  // Check if the clicked element is inside the .account div
  if (!event.target.closest('.account') && optionsBox.style.display === 'block') {
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

/* JS style for category dropdown */
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

/* JS styling for side bar */
document.addEventListener('DOMContentLoaded', function() {
    const hamburgerIcon = document.getElementById('hamburger-icon');
    const sideBar = document.querySelector('.side-bar');
    const hamburgerCloseIcon = document.getElementById('hamburger-close');

    function toggleSideBar() {
        const computedStyle = window.getComputedStyle(sideBar);
        if (computedStyle.display === 'none') {
            sideBar.style.display = 'flex';
        } else {
            sideBar.style.display = 'none';
        }
    }

    hamburgerIcon.addEventListener('click', function(event) {
        event.stopPropagation();  // Prevent the click event from propagating to the document
        toggleSideBar();
    });

    hamburgerCloseIcon.addEventListener('click', function() {
        sideBar.style.display = 'none';
    });

    // Close the dropdown when clicking outside of it
    document.body.addEventListener('click', function(event) {
        if (!event.target.closest('.side-bar') && sideBar.style.display === 'flex') {
            sideBar.style.display = 'none';
        }
    });
});


/* Ajust or modify window content based on resize */
// Define a function to update content based on window size

// Store the original content of the nav
const originalNavContent = nav.innerHTML;

function updateContent() {
    const nav = document.getElementById('nav');
    const search = document.getElementById('search');
    const windowWidth = window.innerWidth;
    

    if (windowWidth <1000) {
        nav.innerHTML = search.innerHTML; // Change nav content to search content
        
    } else {
        nav.innerHTML = originalNavContent; // Reset nav content
    }
}

// Call the function initially to set the correct state based on initial window size
updateContent();

// Add event listener to call the update content on window resize
window.addEventListener('resize', updateContent);


/* styling for the message alerts */
document.addEventListener("DOMContentLoaded", function() {
    setTimeout(function() {
        const messages = document.querySelectorAll(".pop-up-message");
        messages.forEach(function(message) {
            message.classList.add("hidden");
            setTimeout(() => {
                message.style.display = 'none';
            }, 500); // This matches the transition duration
        });
    }, 5000); // 5 seconds
});


/* styling for otp boxex filling */
document.addEventListener('DOMContentLoaded', function () {
    const otpInputs = document.querySelectorAll('.chakra-pin-input');
    otpInputs.forEach((input, idx) => {
        input.addEventListener('input', () => {
            if (input.value.length > 0) {
                if (idx < otpInputs.length - 1) {
                    otpInputs[idx + 1].focus();
                }
            }
            updateHiddenToken();
        });

        input.addEventListener('keydown', (e) => {
            if (e.key === 'Backspace' && input.value.length === 0 && idx > 0) {
                otpInputs[idx - 1].focus();
            }
        });
    });

    function updateHiddenToken() {
        const token = Array.from(otpInputs).map(input => input.value).join('');
        document.getElementById('hidden-token').value = token;
    }
});


// /* Loading for processing */
document.getElementById('checkout-form').addEventListener('submit', function() {
    const checkoutButton = document.getElementById('checkout-button');
    checkoutButton.disabled = true;
    checkoutButton.innerHTML = 'Processing...';
});