# KisanBazaar

An early frontend prototype of **KisanBazaar** (also referenced as *KisanConnect* in parts of the code) focused on contract farming and farmer-buyer interaction.

This repository preserves the initial static UI exploration designed to connect farmers directly with commercial buyers for contract farming partnerships.

---

## 📌 Project Overview

This is an early-stage static web prototype that demonstrates the conceptual interface and user flows for a direct farmer-to-buyer contracting platform. It is built purely using static web technologies without a live backend or database.

### Implemented Pages & Features

- **`index.html` (Landing Page)**:
  - Hero banner with platform slogan and call-to-action buttons.
  - Informational sections describing platform concepts: Secure Contracts, Guaranteed Payments, Market Intelligence, and Verified Buyers.
  - 4-step workflow overview (*Register & Verify*, *Connect*, *Contract*, *Grow & Earn*).
  - Benefits comparison for farmers and buyers.
  - Header and footer navigation links.

- **`login.html` (Authentication Prototype)**:
  - Form layout with Email and Password inputs using Bootstrap 4 and custom styles.
  - Prototype UI with client-side form controls (no backend authentication connected).

- **`register.html` (User Registration Prototype)**:
  - Role selection dropdown (`Farmer` or `Buyer`).
  - Inputs for full name, email, phone number, location, and password.
  - Prototype JavaScript form submission handler (`event.preventDefault()`) with client-side redirection.

- **`farmerAccount.html` (Farmer Account View)**:
  - Prototype landing dashboard for farmers with standard top navigation.

- **`buyerAccount.html` (Buyer Account View)**:
  - Prototype landing dashboard for buyers with standard top navigation.

- **`styles.css` (Styles & UI Layouts)**:
  - Custom CSS custom properties (color variables), responsive layouts, keyframe animation (`slideBackground`), and mobile media queries.

---

## 🛠️ Technology Stack

- **HTML5**: Page structure and semantic layout.
- **CSS3 / Vanilla CSS**: Custom styling, animations, and responsive rules.
- **Bootstrap 4.5.2 (CDN)**: Layout styling for authentication and registration pages.
- **JavaScript**: Basic inline prototype event handling and page redirection.

---

## 🚀 Running Locally

Because this project is a purely static prototype, no build tools or package managers are required.

Simply open `index.html` in any modern web browser or serve it with a local static file server:

```bash
# Using Python 3 HTTP server
python -m http.server 8000
```
Then visit `http://localhost:8000`.

---

## 📜 Historical Note

This code represents the historical/first stage of the KisanBazaar project and is preserved as an early frontend prototype. Real payment gateways, digital contract signing engines, user verification, and database-backed services were planned concepts not yet integrated at this stage.
