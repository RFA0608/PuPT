import time
import multiprocessing
import subprocess
import sys
sys.path.append(r"py")

pack_prog = './pack'
unpack_prog = './unpack'

import tcp_protocol_server as tcs

HOST = 'localhost'
PORT = 9999

def launch_pack():
    time.sleep(0.01)
    subprocess.run([pack_prog])

def launch_unpack():
    time.sleep(0.01)
    subprocess.run([unpack_prog])    

def pack_main(data):
    packed_data = []

    with tcs.tcp_server(HOST, PORT) as tcsp:
        # send poly_degree and plain_modulus(bits)
        tcsp.send(8192)
        tcsp.send(24)

        # send the number of data
        tcsp.send(len(data))
        for i in range(len(data)):
            tcsp.send(f"{data[i]}")

        # receive poly_size and packed ring coefficient
        _, k = tcsp.recv()
        for i in range(k):
            _, recv_data = tcsp.recv()
            packed_data.append(int(recv_data))

    return packed_data

def unpack_main(packed_data, datalen):
    data = []

    with tcs.tcp_server(HOST, PORT) as tcsp:
        # send poly_degree and plain_modulus(bits)
        tcsp.send(8192)
        tcsp.send(24)

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
    
    return data

if __name__ == "__main__":
    # example
    data = [3, 4, 5]
    datalen = 3

    p = multiprocessing.Process(target=launch_pack)
    p.start()
    pack_data = pack_main(data)
    
    p.join()

    up = multiprocessing.Process(target=launch_unpack)
    up.start()
    recv_data = unpack_main(pack_data, datalen)
    
    up.join()

    for i in range(datalen):
        print(f"{recv_data[i]}")