# Multi client chat - CHAT by Fabrymus

import sys, socket, select
 
def chat_client():
    if(len(sys.argv) < 3) :
        print '[*] - Usage - python chat_client.py << host >> << port >>'
        sys.exit()
	
    host = sys.argv[1]
    try:
    	port = int(sys.argv[2])
    except:
	print "[-] - Inserire un valore di porta valido\n"
	sys.exit("[-] - Exited")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # Mi connetto all'host remoto
    try :
        s.connect((host, port))
    except :
        print '[-] - Impossibile Connettersi'
        sys.exit()
     
    print "Connesso all'host remoto. Puoi iniziare a messaggiare!"
    sys.stdout.write('[ IO ] > '); sys.stdout.flush()
     
    while 1:
        socket_list = [sys.stdin, s]
         
        # Prendo la lista dei socket leggibili
        da_leggere, da_scrivere, error_sockets = select.select(socket_list , [], [])
         
        for sock in da_leggere:            
            if sock == s:
                # Messaggio in arrivo dal server s
                data = sock.recv(4096)
                if not data :
                    print '\n[-] - Disconnesso dalla chat..'
                    sys.exit()
                else :
                    #Stampo il messaggio
                    sys.stdout.write(data)
                    sys.stdout.write('[ IO ] > '); sys.stdout.flush()     
            
            else :
                # Un utente ha inserito un messaggio
                msg = sys.stdin.readline()
                s.send(msg)
                sys.stdout.write('[ IO ] > '); sys.stdout.flush() 

if __name__ == "__main__":
#Evito errori di loop
    sys.exit(chat_client())

