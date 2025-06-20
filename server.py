import sqlite3
import argparse
from mcp.server.fastmcp import FastMCP

mcp = FastMCP('sqlite-mcp')

def init_db():
    conn = sqlite3.connect('mcp_data.db')
    cursor = conn.cursor()
    cursor.execute(
        ''' CREATE TABLE IF NOT EXISTS people (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                profession TEXT NOT NULL
            )
        '''
    )
    conn.commit()
    return conn, cursor

@mcp.tool()
def add_data(query: str) -> bool:
    """ Add new data to the people table using a SQL insert query.

    Args:
        query (str): SQL INSERT query following this format:
        INSERT INTO people (name, age, profession)
        VALUES ('Jhon Doe', 30, 'Engineer')

    Schema:
        - name: Text field (required)
        - age: Integer field (required)
        - profession: Text field (required)
        Note: 'id' field is auto-generated

    Returns:
        bool: True if data was added successfully, False otherwise

    Example:
        >>> query = '''
        ... INSERT INTO people (name, age, profession)
        ... VALUES ('Virat Kohli', 37, 'Cricketer')
        ... '''
        >>> add_data(query)
        True
    """

    conn, cursor = init_db()
    try:
        cursor.execute(query)
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error adding data: {e}")
        return False
    finally:
        conn.close()

@mcp.tool()
def read_data(query: str="SELECT * FROM people") -> list:
    """Read data from the people table using a SQL SELECT query.

    Args:
        query (str, optional): SQL SELECT query. Default is "SELECT * FROM people"
        Examples:
            - "SELECT * FROM people"
            - "SELECT name, age FROM people WHERE age > 25"
            - "SELECT * from people ORDER BY age DESC"

    Returns:
        list: List of tuples containing the query results.
            for default query, tuple format is (id, name, age, profession)

    Example:
        >>> # Read all records
        >>> read_data()
        [(1, 'Jhon Doe', 30, 'Engineer'), (2, 'Virat Kohli', 37, 'Cricketer')]

        >>> # Read with custom query
        >>> read_data("SELECT name, profession FROM people WHERE age > 30")
        [('Virat Kohli', 'Cricketer')]
    """

    conn, cursor = init_db()
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error reading data: {e}")
        return []
    finally:
        conn.close()

if __name__ == "__main__":
    print("Starting server...")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--server_type", type=str, default="sse", choices=["sse", "stdio"]
    )

    args = parser.parse_args()
    mcp.run(args.server_type)
