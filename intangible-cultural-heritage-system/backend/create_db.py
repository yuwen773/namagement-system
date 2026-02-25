"""
Script to create the heritage_db database
"""
import MySQLdb

try:
    # Connect to MySQL server (without specifying database)
    connection = MySQLdb.connect(
        host='127.0.0.1',
        user='root',
        password='yuwen123.',
        port=3306
    )
    
    cursor = connection.cursor()
    
    # Create database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS heritage_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    print("✓ Database 'heritage_db' created successfully!")
    
    # Show databases to verify
    cursor.execute("SHOW DATABASES LIKE 'heritage_db'")
    result = cursor.fetchone()
    if result:
        print(f"✓ Verified: Database '{result[0]}' exists")
    
    cursor.close()
    connection.close()
    
except MySQLdb.Error as e:
    print(f"✗ Error: {e}")
    print("\nPlease check:")
    print("  1. MySQL server is running")
    print("  2. Username and password are correct")
    print("  3. User has CREATE DATABASE privilege")
