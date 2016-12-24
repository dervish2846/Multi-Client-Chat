# Multi Client chat - Server by fabrymus
 
import sys, socket, select

HOST = '' 
lista_socket = []
rcv_buffer = 4096 
PORT = 9009 #default

#verifico se e' stata inserita un'altra porta
def init_args():
	if len(sys.argv) != 2:
		print "[*] - Usage - python server.py <port>\n"
		print "[*] - Porta non specificata!\n"
		print "[*] - Server della chat partito usando la porta di default 9009\n"
		pass
#passo
	else:
		PORT = sys.argv[1]

def chat_server():
    init_args()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
 
    # Aggiungo il server socket nella lista delle connessioni disponibili
    lista_socket.append(server_socket)
 
    print "[*] - Server della chat partito nella porta:" + str(PORT)
 
    while 1:
        # Prendo le list pronte per essere lette e selezionate da select
 	# il 4_o argomento indico il time_out = 0 ovvero mai in blocco
        da_leggere,da_scrivere,error_in = select.select(lista_socket,[],[],0)
      
        for sock in da_leggere:
            # Ho ricevuto una nuova connessione
            if sock == server_socket: 
                connessione, addr = server_socket.accept()
                lista_socket.append(connessione)
                print "[*] - Il Client [%s, %s] si e' appena connesso!" % addr
                broadcast(server_socket, connessione, "[*] - [%s:%s] e' entrato nella chat room!\n" % addr)
             
            # Non ho una nuova connessione ma un nuovo messaggio da un client gia connesso
            else:
                # Processo i dati ricevuti
                try:
                    # Ricevo i dati dal socket
                    data = sock.recv(rcv_buffer)
                    if data:
			print "["+str(sock.getpeername())+"]"+" > "+data
                        # Effettuo il broadcast
                        broadcast(server_socket, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + data)  
                    else:
                        # Rimuovo il socket che e' danneggiato    
                        if sock in lista_socket:
                            lista_socket.remove(sock)

                        # In questa fase non necessariamente il client si e' disconnesso..
                        broadcast(server_socket, sock, "[-] - Il Client [%s, %s] e' offline\n" % addr) 
                # Eccezzioni 
                except:
                    broadcast(server_socket, sock, "[-] - Il Client [%s, %s] e' offline\n" % addr)
                    continue

    server_socket.close()
    
# Effettuo il broadcast del messaggio a tutti i client connessi al server
def broadcast (server_socket, sock, message):
    for socket in lista_socket:
        # Invio il messaggio a tutti i peer, verificando che non lo sto inviando allo stesso client
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # E' caduta la connessione al socket
                socket.close()
                # Rimuovo la connessione scaduta
                if socket in lista_socket:
                    lista_socket.remove(socket)
 
if __name__ == "__main__":
#evito guasti di loop uscendo
    sys.exit(chat_server())


         
