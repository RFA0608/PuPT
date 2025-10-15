import sys
sys.path.append(r"py")
import PnUP as pnup

def main():
    # example
    data = [3, 4, 5]
    datalen = 3

    pack_data = pnup.pack_main(data)
    
    recv_data = pnup.unpack_main(pack_data, datalen)

    for i in range(datalen):
        print(f"{recv_data[i]}")

if __name__ == "__main__":
    main()