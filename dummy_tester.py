from django.utils.six.moves import urllib, socketserver as SocketServer


protocol_data = "<protokol><runLog><test><name>01.in</name><resultCode></resultCode><resultMsg>OK</resultMsg><time>0</time><details></details><score></score></test><score>100</score><details></details><finalResult>1</finalResult><finalMessage>OK</finalMessage></runLog></protokol>"


class Testovac(SocketServer.BaseRequestHandler):
    def handle(self):
        input_data = self.request.recv(1024 * 1024).strip()
        print("Connection from: " + str(self.client_address))
        self.request.close()

        data_str = input_data.decode('utf8')
        data_obj = data_str.split('\n', 6)
        submit_id = data_obj[1]

        data = urllib.parse.urlencode({
            "submit_id": int(submit_id),
            "protocol": protocol_data
        }).encode('utf-8')
        url = "http://127.0.0.1:8000/submit/receive_protocol/"

        req = urllib.request.Request(url, data)
        urllib.request.urlopen(req)

if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 12347
    server = SocketServer.TCPServer((HOST, PORT), Testovac)
    server.serve_forever()
    print("Running!")
