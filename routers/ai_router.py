from fastapi import APIRouter
from pydantic import BaseModel
from openai import OpenAI
import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/ai", tags=["AI"])

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# SQL Server connection
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=pos_system;"
    "Trusted_Connection=yes;"
)
def get_db_schema():
    cursor = conn.cursor()
    schema = {}

    # Get all user tables
    cursor.execute("""
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_TYPE='BASE TABLE' AND TABLE_CATALOG='pos_system';
    """)
    tables = [row[0] for row in cursor.fetchall()]

    for table in tables:
        cursor.execute(f"""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = '{table}';
        """)
        columns = [row[0] for row in cursor.fetchall()]
        schema[table] = columns

    return schema
class Question(BaseModel):
    question: str

@router.post("/ask")
async def ask_database(data: Question):
    try:
        schema = get_db_schema()
        schema_text = "\n".join([f"{table}: {', '.join(cols)}" for table, cols in schema.items()])

        prompt = f"""
        You are a SQL Server expert.
        Database schema is as follows:
        {schema_text}

        Convert the following question into a SQL SELECT query using **only the tables and columns above**.
        Only generate SELECT queries. No DELETE, UPDATE, INSERT, DROP.
        Return SQL only. No markdown.
        Question:
        {data.question}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        import re
        sql_query = response.choices[0].message.content.strip()
        sql_query = re.sub(r"```sql|```", "", sql_query, flags=re.IGNORECASE).strip()

        if not sql_query.lower().startswith("select"):
            return {"error": "Only SELECT queries allowed", "query": sql_query}

        # Optional extra security check
        for forbidden in ["insert", "update", "delete", "drop", "alter", "exec", "xp_"]:
            if forbidden in sql_query.lower():
                return {"error": "Dangerous SQL detected"}

        cursor = conn.cursor()
        cursor.execute(sql_query)
        columns = [c[0] for c in cursor.description]
        rows = cursor.fetchall()
        results = [dict(zip(columns, row)) for row in rows]

        return {
            "generated_sql": sql_query,
            "data": results
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}