import time
import multiprocessing
import subprocess

pack_prog = './cpp/pack'
unpack_prog = './cpp/unpack'

import tcp_protocol_server as tcs

HOST = 'localhost'
PORT = 9999

class pupt:
    Poly_Degree = 2**13
    Plain_Modulus = 24
    Plain_Modulus_Specify = -1

    def __init__(self, poly_d, plain_b):
        self.Poly_Degree = poly_d
        self.Plain_Modulus = plain_b
        self.Plain_Modulus_Specify = -1

    def set_entry(self, poly_d, plain_b):
        self.Poly_Degree = poly_d
        self.Plain_Modulus = plain_b
    
    def launch_pack(self):
        time.sleep(0.01)
        subprocess.run([pack_prog])

    def launch_unpack(self):
        time.sleep(0.01)
        subprocess.run([unpack_prog])    

    def pack(self, data):
        packed_data = []

        p = multiprocessing.Process(target=self.launch_pack)
        p.start()

        with tcs.tcp_server(HOST, PORT) as tcsp:
            # send poly_degree and plain_modulus(bits)
            tcsp.send(self.Poly_Degree)
            tcsp.send(self.Plain_Modulus)
            _, get_plain_modulus = tcsp.recv()
            self.Plain_Modulus_Specify = int(get_plain_modulus)

            # send the number of data
            tcsp.send(len(data))
            for i in range(len(data)):
                tcsp.send(f"{data[i]}")

            # receive poly_size and packed ring coefficient
            _, k = tcsp.recv()
            for i in range(k):
                _, recv_data = tcsp.recv()
                packed_data.append(int(recv_data))

        p.join()

        return packed_data

    def unpack(self, packed_data, datalen):
        data = []

        up = multiprocessing.Process(target=self.launch_unpack)
        up.start()

        with tcs.tcp_server(HOST, PORT) as tcsp:
            # send poly_degree and plain_modulus(bits)
            tcsp.send(self.Poly_Degree)
            tcsp.send(self.Plain_Modulus)

            # send the number of data
            k = datalen
            tcsp.send(k)

            # send the number of packed_data
            for i in range(len(packed_data)):
                tcsp.send(f"{packed_data[i]}")

            # receive data
            recv_unpacked_data = -1
            for i in range(k):
                _, recv_unpacked_data = tcsp.recv()
                data.append(recv_unpacked_data)

        up.join()
        
        return data