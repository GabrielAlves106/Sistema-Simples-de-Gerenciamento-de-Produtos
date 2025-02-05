import sqlite3

banco_principal = sqlite3.connect("banco.db")

cursor = banco_principal.cursor()

#cursor.execute("CREATE TABLE produtos (IDproduto integer, NOMEproduto text, QUANTIDADEproduto integer, DATAVALIDADEproduto text)") 
#cursor.execute("CREATE TABLE usuarios (IDuser interger, SENHAuser integer, NOMEuser text, NOMElogin text )")

cursor.execute("CREATE TABLE estoque (IDproduto INTEGER PRIMARY KEY, NOMEproduto TEXT, QUANTIDADEproduto INTEGER, DATAVENCIMENTOproduto DATE NOT NULL )")
