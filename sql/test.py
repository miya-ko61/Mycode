import pyodbc

# 数据库文件路径
db_path = 'tmp.accdb'

# 连接字符串
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=' + db_path + ';'
)

def connect_db():
    """连接到Access数据库"""
    try:
        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def get_table_names(conn):
    """获取所有用户表的表名"""
    cursor = conn.cursor()
    table_names = []
    try:
        # 查询系统表以获取用户表名
        cursor.execute("SELECT Name FROM MSysObjects WHERE Type=1 AND Flags=0")
        for row in cursor.fetchall():
            table_names.append(row[0])
    except Exception as e:
        print(f"Error fetching table names: {e}")
    finally:
        cursor.close()
    return table_names

def get_table_structure(conn, table_name):
    """获取指定表的结构"""
    cursor = conn.cursor()
    try:
        # 查询表的列信息
        cursor.execute(f"SELECT * FROM {table_name} WHERE 1=0")  # 获取列信息
        columns = [column[0] for column in cursor.description]
        print(f"Table: {table_name}, Columns: {columns}")
    except Exception as e:
        print(f"Error fetching table structure for {table_name}: {e}")
    finally:
        cursor.close()

def main():
    conn = connect_db()
    if conn:
        # 获取并打印所有表名
        table_names = get_table_names(conn)
        if table_names:
            print("Tables in the database:")
            for table_name in table_names:
                print(f" - {table_name}")
                # 获取并打印表结构
                get_table_structure(conn, table_name)
        else:
            print("No user tables found in the database.")
        conn.close()
    else:
        print("Failed to connect to the database.")

if __name__ == "__main__":
    main()
