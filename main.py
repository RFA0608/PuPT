import sys
sys.path.append(r"py")
import PnUP as pnup

def main():
    # example
    pup = pnup.pupt(2**13, 24)

    data = [3, 4, 5, 6, 7, 8]
    datalen = 6

    pack_data = pup.pack(data)
    
    recv_data = pup.unpack(pack_data, datalen)

    print(f"{pup.Plain_Modulus_Specify}")

    for i in range(datalen):
        print(f"{recv_data[i]}")

if __name__ == "__main__":
    main()