# Valve Inventory Management System

A simple Flask web app for tracking industrial valve stock using SKU codes built from valve attributes.

---

## Features

- **Inventory view** – see all items and their current quantities
- **Add items** – generate SKUs from valve attributes (type, class, size, end type, face)
- **Stock In / Out** – adjust quantities with a single click
- **Transaction log** – full history of all stock movements

---

## Project Structure

```
project/
├── app.py          # Main Flask application
├── database.db     # SQLite database (auto-created on first run)
└── templates/
    ├── inventory.html
    ├── add_item.html
    └── transaction.html
```

---

## Setup & Run

**1. Install dependencies**
```bash
pip install flask
```

**2. Run the app**
```bash
python app.py
```

**3. Open in your browser**
```
http://127.0.0.1:5000
```

The database is created and seeded automatically on first run — no setup needed.

---

## SKU Structure

SKUs are generated from the following attributes:

| Attribute | Examples |
|-----------|---------|
| Sub Type  | Ball Valve, Plug Valve, Gate Valve |
| Class     | 150, 300, 600 |
| Size      | 1", 2", 3", 4" |
| End Type  | Flange, Weld |
| Face      | RTJ, RF |

---

## Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | View all inventory |
| `/add-item` | GET, POST | Add a new SKU |
| `/stock-in` | POST | Add stock to an item |
| `/stock-out` | POST | Remove stock from an item |
| `/transactions` | GET | View transaction history |
