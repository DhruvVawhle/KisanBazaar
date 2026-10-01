# KisanBazaar

> An agricultural commerce ecosystem connecting farmers directly with consumers and commercial buyers.

---

## Project Overview

**KisanBazaar** is an agricultural marketplace platform designed to bridge the gap between farmers, consumers, and commercial buyers. The project eliminates unnecessary middlemen, ensures fair pricing for agricultural producers, and provides consumers with direct access to fresh, high-quality farm produce and groceries.

This repository preserves the complete developmental evolution of KisanBazaar across multiple architectural paradigms:
1. **Old KisanBazaar**: Historical contract-farming frontend prototype.
2. **Current KisanBazaar**: Multi-stage modern implementations encompassing a **PyQt6 desktop grocery application**, a **full-stack web application architecture (React / Express / Drizzle ORM)**, and a **Flask produce listing & price negotiation prototype**.

---

## Project Evolution

```
+-----------------------------------------------------------------------------+
¦                                 KisanBazaar                                 ¦
+-----------------------------------------------------------------------------+
                                       ¦
           +-------------------------------------------------------+
           ?                                                       ?
   Old KisanBazaar                                         Current KisanBazaar
+-------------------------+               +-------------------------------------------------+
¦ Stage 1: Early Frontend ¦               ¦ Stage 2: Multi-Platform Modern Implementations  ¦
¦  - Contract Farming     ¦               +-------------------------------------------------¦
¦  - Static Web Prototype ¦               ¦  PyQt6 Desktop  ¦ Web KB Stack  ¦ Flask Market  ¦
¦  - HTML5 / CSS3 / JS    ¦               ¦  - Grocery GUI  ¦ - React / TS  ¦ - Negotiation ¦
+-------------------------+               ¦  - PDF Invoices ¦ - Express API ¦ - In-Memory   ¦
                                          ¦  - Local Cart   ¦ - Drizzle ORM ¦ - HTML Forms  ¦
                                          +-------------------------------------------------+
```

The repository is structured to maintain clear historical continuity:
- **`Old KisanBazaar/`** documents the initial static vision focused on contract farming partnerships.
- **`KisanBazaar/`** contains the current codebase comprising desktop, full-stack web, and lightweight Python web prototypes.

---

## Implementations in this Repository

| Directory / Module | Implementation Type | Technologies | Primary Purpose | Status |
| :--- | :--- | :--- | :--- | :--- |
| **`Old KisanBazaar/`** | Static Web Frontend | HTML5, CSS3, Bootstrap 4, JS | Contract farming & buyer-farmer portal prototype | Historical Prototype |
| **`KisanBazaar/Kisan Bazaar/`** | Desktop Application | Python 3, PyQt6, QtPrintSupport | Interactive grocery shop, catalog, cart, billing & PDF export | Functional Desktop App |
| **`KisanBazaar/Web KB/`** | Full-Stack Web Architecture | TypeScript, React, Express, Drizzle ORM | Modern web API & client architecture for agricultural commerce | Architecture / Modular Source |
| **`KisanBazaar/` (Flask)** | Lightweight Web Prototype | Python 3, Flask, Jinja2, HTML5 | Produce listing and buyer price negotiation prototype | Functional Prototype |

---

## 1. Old KisanBazaar (Historical Frontend Prototype)

The **Old KisanBazaar** directory preserves the original static web prototype (initially developed under the concept *KisanConnect* / *KisanBazaar*). It focused on facilitating long-term contract farming partnerships between agricultural producers and institutional or bulk buyers.

### Key Pages & Components
- **`index.html` (Landing Page)**:
  - Hero banner with platform mission and call-to-action buttons.
  - Value propositions: *Secure Contracts*, *Guaranteed Payments*, *Market Intelligence*, and *Verified Buyers*.
  - 4-step workflow overview (*Register & Verify*, *Connect*, *Contract*, *Grow & Earn*).
  - Benefits matrix contrasting advantages for farmers and commercial buyers.
- **`login.html`**:
  - Authentication form interface styled with Bootstrap 4 and custom CSS.
- **`register.html`**:
  - Registration form with role selection (`Farmer` vs. `Buyer`) and client-side redirection script.
- **`farmerAccount.html`**:
  - Farmer dashboard placeholder layout.
- **`buyerAccount.html`**:
  - Buyer dashboard placeholder layout.
- **`styles.css`**:
  - Color variable definitions, card grids, media queries, and keyframe animations (`slideBackground`).
- **Image Assets**:
  - `background1.jpg`, `background2.jpg`, `background3.jpg.jpg`.

---

## 2. Current KisanBazaar Implementations

The **`KisanBazaar/`** folder represents subsequent development phases and contains three distinct implementations:

### A. Python / PyQt6 Desktop Application (`Kisan Bazaar/`)
A functional desktop shopping application built with PyQt6.
- **Welcome / Intro Screen**: Visual greeting with branding, tagline, and transition to the shop.
- **Product Catalog**: Renders produce cards from `products.json` with item images, titles, pricing, and unit measurements.
- **Category Filtering & Search**: Instant filtering across categories (*Leafy Vegetables*, *Lentils*, *Dairy & Everyday*) and search by produce name.
- **Cart Management**: Dynamic cart sidebar displaying selected items, quantities, and auto-updating order totals. Includes stock validation against available inventory.
- **Payment & Checkout**:
  - Modal payment selector: **Cash**, **Card**, and **UPI**.
  - Card payment collects cardholder details via dialog.
  - UPI payment presents a scan-to-pay dialog looking for `upi_qr.png`.
  - Simulates a 2.5-second payment transaction delay.
- **Billing & PDF Invoice Export**:
  - Formats an itemized invoice.
  - Appends order records to a local billing ledger (`customer_bill.txt`).
  - Exports professional PDF invoices using `QPrinter` and `QTextDocument`.
- **Order History Viewer**: In-app dialog reading and displaying past purchase records.

### B. Modern Full-Stack Web Application Architecture (`Web KB/`)
A modern full-stack web application architecture containing React, Express, TypeScript, Drizzle ORM, API routes, and frontend components:
- **Database Schema (`backend files/shared/schema.ts`)**:
  - PostgreSQL table definitions via **Drizzle ORM**: `users`, `products`, `orders`.
  - Type definitions and Zod validation schemas (`CartItem`, `insertOrderSchema`).
- **Express API Server (`backend files/shared/server/routes.ts`)**:
  - `GET /api/products`: Search products by keyword or filter by category.
  - `GET /api/categories`: Returns unique product categories.
  - `POST /api/orders`: Validates payload against Zod schema and records new orders.
- **In-Memory Storage Layer (`backend files/shared/server/storage.ts`)**:
  - `MemStorage` class implementing `IStorage` interface with automated bootstrapping from attached JSON catalog data.
- **React Frontend (`frontend files/client/src/App.tsx`)**:
  - Application entry point utilizing `wouter` for routing, `@tanstack/react-query` for asynchronous server state, and accessible UI component wrappers.
- *Note*: `Web KB/` also includes a bundled copy of the PyQt6 desktop assets and image catalog for reference.

### C. Flask Produce Listing & Price Negotiation Prototype (`app.py`)
A Python web prototype exploring dynamic price bargaining between farmers and buyers:
- **`GET /`**: Renders the farmers market produce board (`templates/index.html`).
- **`GET, POST /list_produce`**: Accepts farmer submissions (`item`, `price`) and appends them to the session produce list.
- **`GET, POST /negotiate_price/<int:produce_id>`**: Allows buyers to submit counter-offers for a specific listing (`templates/negotiate_price.html`), updating listed prices.
- **Styling (`static/styles.css`)**: Clean green-accented typography and minimalist card styling.

---

## ??? Technology Stack

| Domain | Technologies |
| :--- | :--- |
| **Desktop GUI** | Python 3, PyQt6, QtPrintSupport |
| **Web Frontend** | React, TypeScript, Wouter, TanStack React Query, HTML5, CSS3, Bootstrap 4 |
| **Backend & APIs** | Node.js, Express, Flask, Jinja2 |
| **Database & ORM** | PostgreSQL schema definitions via Drizzle ORM, Zod validation, In-memory Maps |
| **Data Formats** | JSON (`products.json`), Text (`customer_bill.txt`) |

---

## Repository Structure

```
KisanBazaar/
¦
+-- .gitignore                          # Global repository exclusions
+-- README.md                           # Comprehensive project documentation
¦
+-- Old KisanBazaar/                    # Historical contract-farming frontend
¦   +-- background1.jpg
¦   +-- background2.jpg
¦   +-- background3.jpg.jpg
¦   +-- buyerAccount.html
¦   +-- farmerAccount.html
¦   +-- index.html
¦   +-- login.html
¦   +-- register.html
¦   +-- styles.css
¦
+-- KisanBazaar/                        # Current multi-platform implementations
    ¦
    +-- Kisan Bazaar/                   # PyQt6 Desktop Application
    ¦   +-- images/                     # 28 produce image assets
    ¦   +-- cart_icon.png               # Shopping cart UI asset
    ¦   +-- customer_bill.txt           # Local text billing ledger
    ¦   +-- grocery_shop.py             # PyQt6 desktop application source
    ¦   +-- products.json               # Product catalogue and pricing data
    ¦
    +-- Web KB/                         # Modern Full-Stack Web Architecture
    ¦   +-- backend files/
    ¦   ¦   +-- shared/
    ¦   ¦       +-- schema.ts           # Drizzle ORM PostgreSQL schema & types
    ¦   ¦       +-- server/
    ¦   ¦           +-- routes.ts       # Express REST API endpoints
    ¦   ¦           +-- storage.ts      # In-memory storage implementation
    ¦   +-- frontend files/
    ¦   ¦   +-- client/
    ¦   ¦       +-- src/
    ¦   ¦           +-- App.tsx         # React root application component
    ¦   +-- images/                     # Produce image assets
    ¦   +-- cart_icon.png
    ¦   +-- customer_bill.txt
    ¦   +-- grocery_shop.py
    ¦   +-- products.json
    ¦
    +-- static/                         # Flask prototype static styles
    ¦   +-- styles.css
    +-- templates/                      # Flask prototype Jinja2 templates
    ¦   +-- index.html
    ¦   +-- list_produce.html
    ¦   +-- negotiate_price.html
    +-- app.py                          # Flask produce listing & negotiation server
```

---

## Setup and Run Instructions

### 1. Old KisanBazaar (Static Prototype)
Open any HTML file directly in your web browser, or serve it locally:
```bash
cd "Old KisanBazaar"
python -m http.server 8000
```
Then navigate to `http://localhost:8000`.

---

### 2. PyQt6 Desktop Application
Ensure Python 3.9+ is installed, then install PyQt6:
```bash
pip install PyQt6
```
Run the desktop application from its directory so that relative asset paths resolve:
```bash
cd "KisanBazaar/Kisan Bazaar"
python grocery_shop.py
```

---

### 3. Flask Price Negotiation Prototype
Ensure Flask is installed:
```bash
pip install flask
```
Run the application server from the `KisanBazaar` directory:
```bash
cd "KisanBazaar"
python app.py
```
Open `http://localhost:5000` in your web browser.

---

### 4. Web KB Architecture
The files in `KisanBazaar/Web KB/` provide the core TypeScript definitions, API routes, and React shell. To deploy or integrate this stack in a Node.js project:
- Integrate `schema.ts`, `routes.ts`, and `storage.ts` into an Express + Drizzle backend.
- Connect `App.tsx` into a Vite or Next.js React frontend with Tailwind CSS and Radix UI primitives.

---

## Known Limitations & Scope Notes

To provide an accurate technical assessment of the repository:
1. **Mocked Payment Processing**: The PyQt6 desktop app simulates payment delays and presents local dialogs for UPI and Card details; it does not connect to live banking APIs.
2. **Volatile In-Memory State**: The Flask negotiation prototype stores produce listings in a Python list (`produce_list = []`), meaning data resets upon server restart.
3. **Empty Template**: `templates/list_produce.html` in the Flask prototype is an empty 0-byte file in the source repository; produce additions redirect directly to the index view.
4. **Architectural Web Files**: The `Web KB` folder contains essential schema, route, and UI source files rather than a standalone self-contained npm package build.
5. **Static Authentication**: Login and registration forms in `Old KisanBazaar` perform client-side mock redirections without password hashing or persistent session management.

---

## Future Development Possibilities

- **Unified Omnichannel Platform**: Integrating the PyQt6 desktop POS with the web backend via shared REST/GraphQL APIs.
- **Production Persistence**: Connecting the Drizzle ORM schema to a live PostgreSQL database cluster with migrations.
- **Payment Gateway Integration**: Adding authentic payment processing via Razorpay, Stripe, or direct UPI payment links.
- **Real-Time Bidding & WebSockets**: Enhancing the negotiation engine with real-time price updates between farmers and buyers.
- **Role-Based Access Control**: Implementing multi-tenant authentication for Farmers, Wholesale Buyers, and Retail Consumers.

---

## Author

**Dhruv Vawhle**
- GitHub: [@DhruvVawhle](https://github.com/DhruvVawhle)
