from flask import Flask, jsonify
from db import get_snowflake_connection

app = Flask(__name__)

@app.route('/')
def home():
  return "API Flask connected to Snowflake"

@app.route('/categories')
def get_categories():
  conn = get_snowflake_connection()
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM categories")
  results = cursor.fetchall()
  cursor.close()
  conn.close()

  categories = [{"id": row[0], "name": row[1], "z_total_items": len(results)} for row in results]
  return jsonify(categories)

if __name__ == '__main__':
  app.run(debug=True)
