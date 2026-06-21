#!/usr/bin/env python3
import sys
import os

# Setup Odoo environment
sys.path.insert(0, '/opt/odoo')

import psycopg2
from passlib.context import CryptContext

# Setup password context - match Odoo's hash method exactly
pwd_context = CryptContext(
    schemes=['pbkdf2_sha512'],
    pbkdf2_sha512__rounds=600000,
    deprecated='auto'
)

# Database connection parameters
DB_HOST = 'odoo-postgres'
DB_PORT = 5432
DB_USER = 'odoo'
DB_PASSWORD = 'odoo'
DB_NAME = 'odoo_development'

# New credentials
NEW_EMAIL = 'hatami391998@gmail.com'
NEW_PASSWORD = 'K@takanlah123'

# Hash password using pbkdf2_sha512
hashed_password = pwd_context.hash(NEW_PASSWORD)

try:
    # Connect to database directly with psycopg2
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cr = conn.cursor()
    
    # Find admin user and partner
    cr.execute("SELECT id, login, partner_id FROM res_users WHERE login='admin' LIMIT 1")
    user_record = cr.fetchone()
    
    if user_record:
        user_id, login, partner_id = user_record
        print(f"✓ Ditemukan user: {login} (ID: {user_id})")
        print(f"✓ Partner ID: {partner_id}")
        
        # Update password in res_users
        cr.execute("""
            UPDATE res_users 
            SET password = %s 
            WHERE id = %s
        """, (hashed_password, user_id))
        
        # Update email in res_partner
        cr.execute("""
            UPDATE res_partner 
            SET email = %s 
            WHERE id = %s
        """, (NEW_EMAIL, partner_id))
        
        conn.commit()
        print(f"✓ Email berhasil diubah menjadi: {NEW_EMAIL}")
        print(f"✓ Password berhasil diubah menjadi: {NEW_PASSWORD}")
        print("\n✓ Akun siap digunakan!")
        print(f"\nLogin dengan:")
        print(f"  Username: admin")
        print(f"  Password: {NEW_PASSWORD}")
        
    else:
        print("✗ User admin tidak ditemukan")
        cr.close()
        conn.close()
        sys.exit(1)
        
    cr.close()
    conn.close()
    
except Exception as e:
    print(f"✗ Error: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
