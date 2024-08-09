# query_logger.py

# Example of predefined queries (can be modified or expanded)
select_all_from_table = "SELECT * FROM your_table_name"
select_specific_columns = "SELECT column1, column2 FROM your_table_name"
join_example = """
SELECT t1.column1, t2.column2
FROM your_table_name t1
JOIN another_table t2 ON t1.id = t2.foreign_id
"""

# Function to dynamically construct queries as needed
def dynamic_query(table_name, columns="*", condition="1=1", join_clause=""):
    """
    Constructs a SQL query with optional columns, condition, and join clause.
    
    :param table_name: Name of the main table.
    :param columns: Columns to select (default is '*').
    :param condition: WHERE clause condition (default is '1=1').
    :param join_clause: JOIN clause to join with another table (default is empty).
    :return: A SQL query string.
    """
    query = f"SELECT {columns} FROM {table_name} "
    
    if join_clause:
        query += f"{join_clause} "
    
    query += f"WHERE {condition}"
    
    return query


from sqlalchemy import create_engine, text
from query_logger import select_all_from_table, dynamic_query

class RowData:
    def __init__(self, data):
        self.__dict__.update(data)

def get_data_with_raw_sql(query):
    # Update with your actual database connection string
    engine = create_engine('oracle+oracledb://username:password@hostname:port/service_name')
    with engine.connect() as conn:
        result = conn.execute(text(query)).fetchone()
        
        if result:
            # Convert the SQLAlchemy row result to a dictionary
            result_dict = dict(result._mapping)
            return RowData(result_dict)
        return None

# Example usage with predefined query
data = get_data_with_raw_sql(select_all_from_table)

if data:
    print("Data from predefined query:")
    for attr, value in data.__dict__.items():
        print(f"{attr}: {value}")
else:
    print("No data found with predefined query")

# Example usage with dynamically constructed query
query = dynamic_query("your_table_name", "column1, column2", "your_table_name.column1 = 'some_value'")
data = get_data_with_raw_sql(query)

if data:
    print("\nData from dynamic query:")
    for attr, value in data.__dict__.items():
        print(f"{attr}: {value}")
else:
    print("No data found with dynamic query")

# Example with dynamic query and join clause
join_clause = "JOIN another_table ON your_table_name.id = another_table.foreign_id"
query = dynamic_query("your_table_name", "column1, column2", "your_table_name.column1 = 'some_value'", join_clause)
data = get_data_with_raw_sql(query)

if data:
    print("\nData from dynamic query with join:")
    for attr, value in data.__dict__.items():
        print(f"{attr}: {value}")
else:
    print("No data found with dynamic query and join")
