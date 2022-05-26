import socket
from numpy import save
from md5 import md5
from rsa import RSAKeyGenerator
from rsa import RSA
from des import mydes as DES

# Create a socket (SOCK_STREAM means a TCP socket)
def SendtoServer(HOST,PORT,data,name):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(bytes(name+':'+data + "\n", "utf-8"))
        # Receive data from the server and shut down
        received = str(sock.recv(1024), "utf-8")
        print("Sent:     {}".format(data))
        print("Received: {}".format(received))

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    savepath=r'I:\homework\crypto_exam\exam3'
    filepath=r'I:\homework\crypto_exam\exam3\test.txt'
    # mykey=RSAKeyGenerator.KeyGenerator()
    e,n=174671,1977533
    key='133457799BBCDFF1'
    data_md5=md5.Encrypto(filepath,savepath)
    SendtoServer(HOST,PORT,data_md5,'md5')
    cipher_key=RSA.RSAEncrypyo(e,n,key,savepath)
    SendtoServer(HOST,PORT,cipher_key,'rsa')
    cipher_text=DES.DesEncrypto(filepath,savepath,int(key,16))
    SendtoServer(HOST,PORT,cipher_text,'des')