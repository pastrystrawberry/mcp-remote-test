
import random
from fastmcp import FastMCP
import os
import sqlite3
import json
DB_PATH=os.path.join(os.path.dirname(__file__),"expenses.db")


mcp = FastMCP(name="ExpenseTracker")
def init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                note TEXT DEFAULT '' 
            )

        """)
init_db()

                    



@mcp.tool
def add_expenses(date,amount, category,subcaetgory="",note=""):
    '''ADD a new expense entry to the database.'''
    with sqlite3.connect(DB_PATH) as c:
        cur=c.execute(
            "INSERT INTO expenses(date,amount, category, subcategory,note)VALUES(?,?,?,?,?)",
            (date, amount,category,subcaetgory,note)
        )
        return {"satus":"ok","id":cur.lastrowid}


@mcp.tool
def list_expenses(start_date,end_date):
    '''list all expense entries from the database with in inclusive date range'''
    with sqlite3.connect(DB_PATH)as c:
        cur=c.execute("SELECT id,date,amount,category,subcategory,note FROM expenses WHERE date BETWEEN ? AND ? ORDER BY id ASC",(start_date, end_date))
        cols=[d[0] for d in cur.description]
        return[dict(zip(cols,r)) for r in cur.fetchall()]
    
@mcp.resource("info://server")
def server_info()->str:
    """Get information about this server."""
    infor={
        "name":"Simple Expense tracker Server",
        "version":"1.0.0",
        "description":"A basic MCP server with expense tools",
        "tools":["add_expenses","list_expenses"],
        "author":"Your Name"
    }
    return json.dumps(info, indent=2)
if __name__=="__main__":
    mcp.run(transport="http",host="0.0.0.0",port=8000)