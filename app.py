from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB = "database.db"

def get_db():
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    db.executescript("""
        CREATE TABLE IF NOT EXISTS sub_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            code TEXT
        );
        CREATE TABLE IF NOT EXISTS classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value INTEGER
        );
        CREATE TABLE IF NOT EXISTS sizes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            size TEXT,
            code TEXT
        );
        CREATE TABLE IF NOT EXISTS end_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            code TEXT
        );
        CREATE TABLE IF NOT EXISTS faces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            code TEXT
        );
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT UNIQUE,
            quantity INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS stock_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT,
            type TEXT,
            quantity INTEGER,
            date TEXT
        );
    """)

    # Seed data only if tables are empty
    if not db.execute("SELECT 1 FROM sub_types LIMIT 1").fetchone():
        db.executescript("""
            INSERT INTO sub_types (name, code) VALUES ('Ball Valve','BV'),('Plug Valve','PV'),('Gate Valve','GV');
            INSERT INTO classes (value) VALUES (150),(300),(600);
            INSERT INTO sizes (size, code) VALUES ('1"','01'),('2"','02'),('3"','03'),('4"','04');
            INSERT INTO end_types (name, code) VALUES ('Flange','F'),('Weld','W');
            INSERT INTO faces (name, code) VALUES ('RTJ','R'),('RF','F');
        """)
    db.commit()
    db.close()

@app.route("/")
def inventory():
    db = get_db()
    items = db.execute("SELECT sku, quantity FROM items ORDER BY sku").fetchall()
    db.close()
    return render_template("inventory.html", items=items)

@app.route("/add-item", methods=["GET", "POST"])
def add_item():
    if request.method == "POST":
        sku = request.form["sku"]
        db = get_db()
        db.execute("INSERT OR IGNORE INTO items (sku, quantity) VALUES (?, 0)", (sku,))
        db.commit()
        db.close()
        return redirect("/")

    db = get_db()
    sub_types = db.execute("SELECT * FROM sub_types").fetchall()
    classes   = db.execute("SELECT * FROM classes").fetchall()
    sizes     = db.execute("SELECT * FROM sizes").fetchall()
    end_types = db.execute("SELECT * FROM end_types").fetchall()
    faces     = db.execute("SELECT * FROM faces").fetchall()
    db.close()
    return render_template("add_item.html",
        sub_types=sub_types, classes=classes,
        sizes=sizes, end_types=end_types, faces=faces)

@app.route("/stock-in", methods=["POST"])
def stock_in():
    sku = request.form["sku"]
    qty = int(request.form["quantity"])
    db = get_db()
    db.execute("UPDATE items SET quantity = quantity + ? WHERE sku = ?", (qty, sku))
    db.execute("INSERT INTO stock_transactions (sku, type, quantity, date) VALUES (?, ?, ?, ?)",
               (sku, "IN", qty, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    db.commit()
    db.close()
    return redirect("/")

@app.route("/stock-out", methods=["POST"])
def stock_out():
    sku = request.form["sku"]
    qty = int(request.form["quantity"])
    db = get_db()
    db.execute("UPDATE items SET quantity = MAX(0, quantity - ?) WHERE sku = ?", (qty, sku))
    db.execute("INSERT INTO stock_transactions (sku, type, quantity, date) VALUES (?, ?, ?, ?)",
               (sku, "OUT", qty, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    db.commit()
    db.close()
    return redirect("/")

@app.route("/transactions")
def transactions():
    db = get_db()
    txns = db.execute("SELECT * FROM stock_transactions ORDER BY id DESC").fetchall()
    db.close()
    return render_template("transaction.html", transactions=txns)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
