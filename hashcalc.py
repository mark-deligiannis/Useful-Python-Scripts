import hashlib
import signal
 
def handler(signum, frame):
    print("\n\nExiting...\n")
    exit(1)
signal.signal(signal.SIGINT,handler)


algs = {"256": hashlib.sha256, "512": hashlib.sha512}
usrinput = input("sha256 (256) or sha512 (512)? ")
while usrinput not in ["256","512"]:
    usrinput = input("sha256 (256) or sha512 (512)? ")

hstring = input("String to be hashed: ")

print("==============================================================")
print(algs[usrinput](hstring.encode()).hexdigest())
print("==============================================================")