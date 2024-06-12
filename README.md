# ePharma eCommerce Website

**ePharma** is an online pharmacy platform built with Django. This project allows users to browse, search, and purchase pharmaceutical products online. It also includes user authentication, cart functionality, and Stripe payment integration.

## Live Demo

Check out the live application: [ePharma Live](https://epharma-91ebb7c041f9.herokuapp.com)

## Features

- **User Registration and Authentication**
- **Browse and Search for Products**
- **Add, Remove, and Update Cart Items**
- **Upload Prescription from doctor or just any drug you cannot find**
- **Checkout with Stripe Payment Integration**
- **Admin Panel for Managing Products and Categories**
- **Password Reset with One-Time Password (OTP)**
- **Responsive Design for Mobile and Desktop**

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/dipec001/onlinestore.git
    cd onlinestore
    ```

2. **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**
    Create a `.env` file in the project root directory and add your environment variables:
    ```env
    SECRET_KEY=your_secret_key
    DEBUG=True
    STRIPE_SECRET_KEY=your_stripe_secret_key
    DOMAIN=http://127.0.0.1:8000  # Or your production domain
    ```

5. **Run database migrations:**
    ```bash
    python manage.py migrate
    ```

6. **Create a superuser:**
    ```bash
    python manage.py createsuperuser
    ```

7. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

8. **Access the application:**
    Open your browser and navigate to `http://127.0.0.1:8000`.

## Usage

### User Authentication

- **Register:** Create a new account by navigating to the registration page.
- **Login:** Access your account by logging in.
- **Logout:** Log out from your account.

### Product Browsing and Searching

- Browse products by categories.
- Use the search bar to find specific products.

### Cart Functionality

- **Add to Cart:** Add products to your cart.
- **View Cart:** View the items in your cart.
- **Update Cart:** Increase or decrease the quantity of items in your cart.
- **Remove from Cart:** Remove items from your cart.

### Checkout and Payment

- **Proceed to Checkout:** Enter your billing details and proceed to Stripe payment.
- **Payment Success:** View the success page after a successful payment.
- **Payment Cancel:** View the cancel page if the payment is canceled.

### Admin Panel

- Access the Django admin panel at `http://127.0.0.1:8000/admin`.
- Manage users, products, and categories.

## Project Structure

``` structure
epharma/
├── epharma/
│ ├── settings.py
│ ├── urls.py
│ ├── wsgi.py
│ └── asgi.py
├── myapp/
│ ├── admin.py
│ ├── apps.py
│ ├── forms.py
│ ├── models.py
│ ├── views.py
│ ├── urls.py
│ ├── templates/
│ │ ├── base.html
│ │ ├── index.html
│ │ ├── login.html
│ │ ├── register.html
│ │ ├── cart.html
│ │ ├── checkout.html
│ │ ├── success.html
│ │ ├── cancel.html
│ │ └── ...
│ └── ...
├── static/
│ ├── css/
│ ├── js/
│ └── images/
├── manage.py
└── requirements.txt
```

## Screenshots

### Home Page
![Home Page](![Screenshot 2024-06-05 095511](https://github.com/Dipec001/onlinestore/assets/119022956/af0b5ddf-22dd-4075-9b29-6fd0436c0505)
)

### Product Page
![Product Page](![Screenshot 2024-06-05 095753](https://github.com/Dipec001/onlinestore/assets/119022956/0b5e0fa5-acae-4622-bf9a-d05968528a9e)
)

### Cart Page
![Cart Page]![Screenshot 2024-06-05 095925](https://github.com/Dipec001/onlinestore/assets/119022956/c7e3de6c-2d52-45e2-87e8-9e0abe8efbbe)


### Upload Prescription Page
![Upload Prescription](![Screenshot 2024-06-05 100113](https://github.com/Dipec001/onlinestore/assets/119022956/aeca48c0-0c64-48d1-b681-df52086255cd)
)

## Contributing

If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are welcome.

1. **Fork the repository.**
2. **Create your feature branch (`git checkout -b feature/AmazingFeature`).**
3. **Commit your changes (`git commit -m 'Add some amazing feature'`).**
4. **Push to the branch (`git push origin feature/AmazingFeature`).**
5. **Open a pull request.**

## License

This project is licensed under the MIT License.
