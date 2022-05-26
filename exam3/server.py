import socketserver
from md5 import md5
from rsa import RSA
from des import mydes as DES

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    n=1977533
    d=1114031
    data_md5=''
    data_rsa=''
    data_des=''
    savepath=r'I:\homework\crypto_exam\exam3\ReceiveFile'
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(bytes("received", "utf-8"))
        msg=self.data.decode('UTF-8')
        msg_name=msg[0:3]
        msg=msg[4:]
        if(msg_name=='md5'): 
            self.data_md5=msg
            self.md5_Decrypto()
        elif(msg_name=='rsa'):
            self.data_rsa=msg
            self.rsa_Decrypto()
        elif(msg_name=='des'):
            self.data_des=msg
            self.des_Decrypto()

    def des_Decrypto(self):
        data_des=self.data_des
        with open(self.savepath+"/des_encrypto.txt","w",encoding="UTF-8") as t:
            t.write(data_des)
        with open(self.savepath+"/rsa_decrypto.txt","r",encoding="UTF-8") as t:
            de_key=t.read()
        with open(self.savepath+"/data_md5.txt","r",encoding="UTF-8") as t:
            data_md5=t.read()
        de_text=DES.DesDecrypto(r'I:\homework\crypto_exam\exam3\ReceiveFile\des_encrypto.txt',self.savepath,int(de_key,16))
        print(de_text)
        de_md5=md5.Encrypto(r'I:\homework\crypto_exam\exam3\ReceiveFile\des_decrypto.txt',self.savepath)
        print("密钥:",de_key)
        print("解密文本:",de_text)
        print("md5:",de_md5)
        if(de_md5==data_md5):print("ok")
        
    def rsa_Decrypto(self):
        d=self.d
        n=self.n
        data_rsa=self.data_rsa
        RSA.RSADecrypyo(d,n,data_rsa,self.savepath)

    def md5_Decrypto(self):
        data_md5=self.data_md5
        with open(self.savepath+"/data_md5.txt","w",encoding="UTF-8") as t:
            t.write(data_md5)
if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()