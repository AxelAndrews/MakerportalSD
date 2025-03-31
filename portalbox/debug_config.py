#!/usr/bin/env python3

import mysql.connector
import configparser
import sys
import os

def test_database_connection(config):
    """Test MySQL database connection"""
    print("Testing Database Connection...")
    try:
        connection = mysql.connector.connect(
            host=config['database']['host'],
            database=config['database']['database'],
            user=config['database']['username'],
            password=config['database']['password']
        )
        print("✅ Database Connection Successful!")
        
        # Check API Keys
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM api_keys LIMIT 5")
        api_keys = cursor.fetchall()
        
        print("\nAPI Keys in Database:")
        for key in api_keys:
            print(f"ID: {key['id']}, Name: {key['name']}")
        
        connection.close()
        return True
    except mysql.connector.Error as err:
        print(f"❌ Database Connection Failed: {err}")
        return False

def test_config_file(config_path):
    """Validate configuration file"""
    print(f"\nTesting Configuration File: {config_path}")
    
    config = configparser.ConfigParser()
    config.read(config_path)
    
    print("\nConfiguration Sections:")
    for section in config.sections():
        print(f"- {section}")
        for key in config[section]:
            # Mask password
            value = config[section][key]
            masked_value = value[:2] + '*' * (len(value) - 4) + value[-2:] if len(value) > 4 else '*' * len(value)
            print(f"  {key}: {masked_value}")
    
    # Specific checks
    checks = {
        'database': ['host', 'database', 'username', 'password'],
        'oauth': ['google_oauth_client_id']
    }
    
    print("\nConfiguration Validation:")
    for section, keys in checks.items():
        if section not in config.sections():
            print(f"❌ Missing section: {section}")
            continue
        
        for key in keys:
            if key not in config[section]:
                print(f"❌ Missing key in {section}: {key}")
            elif not config[section][key] or config[section][key].startswith('YOUR_'):
                print(f"❌ {section}.{key} not configured")
            else:
                print(f"✅ {section}.{key} configured")

def main():
    # Potential config file locations
    config_paths = [
        'config/config.ini',
        '../config/config.ini',
        'config.ini',
        '../config.ini',
        os.path.expanduser('~/portalbox/config.ini')
    ]
    
    config_path = None
    for path in config_paths:
        if os.path.exists(path):
            config_path = path
            break
    
    if not config_path:
        print("❌ No configuration file found!")
        sys.exit(1)
    
    print(f"Using configuration file: {config_path}")
    
    config = configparser.ConfigParser()
    config.read(config_path)
    
    test_config_file(config_path)
    test_database_connection(config)

if __name__ == '__main__':
    main()
