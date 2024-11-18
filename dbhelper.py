from sqlite3 import connect, Row

database:str = 'studentinfo.db' 

def getprocess(sql:str) -> object:
	db:object = connect(database)
	cursor:object = db.cursor()
	cursor.execute(sql)
	cursor.row_factory = Row
	data = cursor.fetchall()
	db.close()
	return data

def postprocess(sql:str) -> bool:
	db:object = connect(database)
	cursor:object = db.cursor()
	cursor.execute(sql)
	db.commit()
	return True if cursor.rowcount > 0 else False

def getall_record(table:str) -> object:
	sql:str = f'SELECT * FROM {table}'
	print("Get All Records: ", sql)
	return getprocess(sql)

def getone_record(table:str, **kwargs) -> object:
	sql:str = f"SELECT * FROM {table} WHERE {list(kwargs.keys())[0]} = '{list(kwargs.values())[0]}'"
	print("Get One Record: ", sql)
	return getprocess(sql)

def delete_record(table:str, **kwargs) -> bool:
	sql:str = f"DELETE FROM {table} WHERE {list(kwargs.keys())[0]} = '{list(kwargs.values())[0]}'"
	print("Delete Record: ", sql)
	return postprocess(sql)

# def add_record(table:str, **kwargs) -> bool:
# 	sql:str = f"INSERT INTO {table} ({','.join(kwargs.keys())}) VALUES({','.join(f"'{w}'" for w in list(kwargs.values()))})"
# 	print("Add Record: ", sql)
# 	return postprocess(sql)

def add_record(table:str, **kwargs) -> bool:
	keys:list = list(kwargs.keys())
	values:list = list(kwargs.values())
	fields:str = "`, `".join(keys)
	data:str = "','".join(values) 
	sql:str = f"INSERT INTO `{table}` (`{fields}`) VALUES('{data}')"
	return postprocess(sql)

def update_record(table:str, **kwargs) -> bool:
	keys:list = list(kwargs.keys())
	values:list = list(kwargs.values())
	fields:list = []
	for i in range(len(keys)-1):
		fields.append(f"{keys[i+1]} = '{values[i+1]}'")
	fields:str = str(', '.join(fields))
	sql:str = f"UPDATE {table} SET {fields} WHERE {keys[0]} = '{values[0]}'"
	print("Update Record: ", sql)
	return postprocess(sql)
