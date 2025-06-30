
arquivo = open("lorem.txt","r")
print(arquivo.read())
arquivo.close()

print("=" * 70)

arquivo = open("lorem.txt","r")
print(arquivo.readline())
arquivo.close()

print("=" * 70)

arquivo = open("lorem.txt","r")
print(arquivo.readlines())
arquivo.close()

print("=" * 70)

arquivo = open("lorem.txt","r")


# tip
while len(linha := arquivo.readline()):
    print(linha)

arquivo.close()