#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, '/opt/odoo')

import psycopg2

# Database connection parameters
DB_HOST = 'odoo-postgres'
DB_PORT = 5432
DB_USER = 'odoo'
DB_PASSWORD = 'odoo'
DB_NAME = 'odoo_development'

try:
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cr = conn.cursor()
    
    # Set module state to uninstalled
    cr.execute("UPDATE ir_module_module SET state = 'uninstalled' WHERE name = 'estate'")
    
    # Drop the table if it exists
    cr.execute("DROP TABLE IF EXISTS estate_property CASCADE")
    
    conn.commit()
    print("✓ Module uninstalled successfully")
    
    cr.close()
    conn.close()
    
except Exception as e:
    print(f"✗ Error: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
