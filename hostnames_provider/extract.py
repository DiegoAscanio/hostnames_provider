#MODULO DE EXTRAÇÃO DE QQ CSV SEPARADO POR |
lines = [line.rstrip('\n') for line in open('dados.txt')]
print(lines)

n = len(lines)

hostname = ""
mac = ""
ip = ""
i = 0

while(i < n-1) :
	array = lines[i].split("|");
	hostname = array[0]
	mac = array[1]
	ip = array[2]
	print("HOSTNAME = ", hostname, "MAC = ", mac,"IP = ", ip)  	
	i = i + 1

