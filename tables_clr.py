import happybase

conn = happybase.Connection('localhost', port=9090)

conn.open()
conn.delete_table('snmp', disable=True)
conn.delete_table('ping', disable=True)
conn.delete_table('ssh', disable=True)
conn.close()

print("TABLES DELETED")