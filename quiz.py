from cryptography.fernet import Fernet


def quiz():
    key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

    # Oh no! The code is going over the edge! What are you going to do?
    message = b'gAAAAABf6FL0PyNd4K3iPj2ZZp4WmyVm1_75pIJeRaffzR1LrSR2wJqfWoOQ7FUQx57CCcR4a5HzYHUCynnOQ8t3mJvEniEbB-HB3'\
    		  b'-HXNw5pbwmArgj3-gGmYgT-IclRRKz1KHmdIbwRiR0h63qe-NbPBYmBBdZ4ljyqiJU7r2_Kv32hJxr_OGXahjosGtIL5NsHYkQMByDw'


    f = Fernet(key)
    r = f.decrypt(message)
    print(r)


if __name__ != "__main__":
    quiz()
