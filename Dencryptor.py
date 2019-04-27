#Dencryptor: Encryption And Decryption Software
#Encryption: AES
#UI: Terminal Interface
#Dependencies:  Python{pyAesCrypt}, System{figlet}
#Created By: BaconBombz
#Version 2.0

###VERSION INFO###
#Version 1.0 Offers Basic Encryption And Decryption
#Version 2.0 Offers Secure File Transfer Over The Internet

#Import Neccessary Libraries
import os, random, struct, string, time, sys, readline, pyAesCrypt, socket, hashlib, getpass
from Crypto.Cipher import AES
#Global Variables Initialization
keyFile = ''  #Key File
dencryptionKey = '' #Key File Contents
bufferSize = 128 * 1024
chunkSize = 16
port = 2221

def longLine():
    print("--------------------------------------------------------------------------------")

def title():
    clear()
    os.system("figlet Dencryptor") #ASCII Title Generator
    longLine()

def clear():
    os.system("clear")

#Main Menu
def main():
    title()
    global dencryptionKey
    #If Key Files In Session Print Key File Under Title
    if (len(keyFile) > 0):
        print("Key File: " + keyFile)
        with open(keyFile, 'r') as keyFileObject:
            dencryptionKey = keyFileObject.read()
        longLine()
    elif (len(keyFile) == 0):
        dencryptionKey = ''
    print("1) Encrypt A File")
    print("2) Decrypt A File")
    print("3) Encrypt A Folder")
    print("4) Decrypt A Folder")
    print("5) Send A Secure File Transfer")
    print("6) Recieve A Secure File Transfer")
    print("7) Generate A 16 Bit Key")
    print("8) Generate A 64 Bit Key")
    print("9) Generate A 128 Bit Key")
    print("10) Add Key File To Session")
    print("11) Remove Key From Session")
    print("0) Exit")
    longLine()
    option = input("Option: ")
    opTree(option)  #Takes Option And Runs It Through The Operation Handler To Change Screens/Functions

#Option Controller For Main Menu
def opTree(option):
    if (option == "1"):
        encryptScreen()
    elif (option == "2"):
        decryptScreen()
    elif (option == "3"):
        encryptFolderScreen()
    elif (option == "4"):
        decryptFolderScreen()
    elif (option == "5"):
        sendFileScreen()
    elif (option == "6"):
        recieveFileScreen()
    elif (option == "7"):
        keyGenScreen(16)    #Generates A 16 Bit Key File
    elif (option == "8"):
        keyGenScreen(64)    #Generates A 64 Bit Key File
    elif (option == "9"):
        keyGenScreen(128)    #Generates A 128 Bit Key File
    elif (option == "10"):
        addKeyScreen()
    elif (option == "11"):
        removeKeyScreen()
    elif (option == "0"):
        clear()
        exit()
    else:
        main()

def sendFileScreen():
    title()
    rHost = input("Reciever's IP: ")
    fileToSend = input("File To Send: ")
    longLine()
    print("Waiting For Reciever's Confirmation...")
    longLine()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((rHost, port))
        sendConfirm = sock.recv(1)
        if (sendConfirm.decode('utf-8') == '1'):
            encryptedFileName = fileToSend + ".dnc"
            pyAesCrypt.encryptFile(fileToSend, encryptedFileName, dencryptionKey, bufferSize)
            with sock,open(encryptedFileName,'rb') as f:
                print("Sending File Name")
                longLine()
                fileToSend = fileToSend + ".dnc"
                sock.sendall(fileToSend.encode() + b'\n')
                time.sleep(0.3)
                print("Sending File Size")
                longLine()
                sock.sendall(f'{os.path.getsize(fileToSend)}'.encode() + b'\n')
                time.sleep(0.3)
                print("Starting Secure Key Exchange")
                print("Sending Modulo")
                mod = ''
                for x in range(3):
                    mod = mod + str(random.randint(1,3))
                sock.sendall(mod.encode() + b'\n')
                time.sleep(0.1)
                print("Sending Base")
                base = ''
                for x in range(3):
                    base = base + str(random.randint(1,3))
                sock.sendall(base.encode() + b'\n')
                print("Generating Private Key")
                privateKey = ''
                for x in range(5):
                    privateKey = privateKey + str(random.randint(1,5))
                time.sleep(0.3)
                print("Generating Equation")
                senderPublicKey = (int(base) ** int(privateKey)) % int(mod)
                time.sleep(0.1)
                print("Recieving Reciever's Public Key")
                recieverPublicKey = sock.recv(8000)
                recieverPublicKey = recieverPublicKey.decode('utf-8')
                time.sleep(0.1)
                print("Sending Public Key")
                sock.sendall(str(senderPublicKey).encode() + b'\n')
                time.sleep(0.1)
                print("Calculating Key")
                sharedKey = str((int(recieverPublicKey) ** int(privateKey)) % int(mod))
                sharedKey = hashlib.sha256(sharedKey.encode())
                sharedKey = sharedKey.hexdigest()
                sharedKey = sharedKey[0:32]
                print("Encrypting Key")
                initVector = 16 * '\x00'
                sharedKey = bytes(str(sharedKey), encoding='utf-8')
                encryptor = AES.new(sharedKey, AES.MODE_CBC, initVector)
                encryptedKey = encryptor.encrypt(dencryptionKey)
                encryptedKey = encryptedKey + (" " * 8).encode()
                encryptedKeySize = str(len(encryptedKey)).encode()
                time.sleep(0.1)
                print("Sending Encryption Key Size")
                sock.sendall(encryptedKeySize + b'\n')
                time.sleep(0.1)
                print("Sending Encryption Key")
                sock.sendall(encryptedKey)
                time.sleep(0.1)
                print("Secure Key Transfer Complete")
                longLine()
                time.sleep(0.1)
                print("Sending Encrypted File")
                longLine()
                while True:
                    data = f.read(chunkSize)
                    if not data: break
                    sock.sendall(data)
                print("File Has Been Sent")
                sock.close()
                null = input("Press Enter To Return To Main Menu")
                mainFunction()
        elif (sendConfirm == 0):
            sock.close()
            print("Reciever Rejected The Connection")
            null = input("Press ENTER To Return To Return To The Main Menu")
            mainFunction()
    except socket.error:
        sock.close()
        print("There Was An Error Connecting To The Reciever")
        null = input("Press ENTER To Return To Return To The Main Menu")
        mainFunction()

def recieveFileScreen():
    global dencryptionKey
    title()
    print("Waiting For Sender To Connect...")
    longLine()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', port))
    sock.listen(1)
    client, addr = sock.accept()
    print(str(addr) + " Wants To Send A File...")
    confirm = input("Would You Like To Recieve The File? [yes/no]: ")
    longLine()
    if (confirm.lower() == "yes"):
        client.send(b'1')
        with client, client.makefile('rb') as clientFile:
            print("Getting File Name")
            fileName = clientFile.readline().strip().decode()
            print("File Name: " + fileName)
            longLine()
            time.sleep(0.3)
            print("Geting File Size")
            length = int(clientFile.readline())
            print("File Size: " + str(length) + " Bytes")
            longLine()
            time.sleep(0.3)
            print("Starting Secure Key Exchange")
            print("Recieving Modulo")
            mod = int(clientFile.readline())
            time.sleep(0.1)
            print("Modulo: " + str(mod))
            print("Receiving Base")
            base = int(clientFile.readline())
            time.sleep(0.1)
            print("Base: " + str(base))
            print("Generating Private Key")
            privateKey = ''
            for x in range(5):
                privateKey = privateKey + str(random.randint(1,5))
            time.sleep(0.3)
            print("Generating Equation")
            recieverPublicKey = (int(base) ** int(privateKey)) % int(mod)
            time.sleep(0.1)
            print("Sending Public Key")
            client.send(str(recieverPublicKey).encode())
            time.sleep(0.1)
            print("Recieving Sender's Public Key")
            senderPublicKey = int(clientFile.readline())
            time.sleep(0.1)
            print("Calculating Key")
            sharedKey = str((int(senderPublicKey ** int(privateKey))) % int(mod))
            sharedKey = hashlib.sha256(sharedKey.encode())
            sharedKey = sharedKey.hexdigest()
            sharedKey = sharedKey[0:32]
            initVector = 16 * '\x00'
            print("Recieving Encryption Key Size")
            encryptedKeySize = clientFile.readline()
            encryptedKeySize = int(encryptedKeySize.decode('utf-8'))
            time.sleep(0.1)
            print("Decrypting Key")
            encryptedKey = clientFile.read(encryptedKeySize)
            initVector = 16 * '\x00'
            sharedKey = bytes(str(sharedKey), encoding='utf-8')
            decryptor = AES.new(sharedKey, AES.MODE_CBC, initVector)
            for x in range(8):
                encryptedKeyPart = encryptedKey[0:16]
                encryptedKey = encryptedKey[16:-1]
                dencryptionKey = dencryptionKey + decryptor.decrypt(encryptedKeyPart).decode('utf-8')
            time.sleep(0.1)
            print("Secure Key Transfer Complete")
            longLine()
            time.sleep(0.1)
            print("Downloading Encrypted File")
            print(("This May Take A While"))
            longLine()
            with open(fileName,'wb') as f:
                while length:
                    chunk = min(length,bufferSize)
                    data = clientFile.read(chunk)
                    if not data: break # socket closed
                    f.write(data)
                    length -= len(data)
            if length != 0:
                print("Download Failed")
            else:
                time.sleep(0.1)
                print("Encrypted File Downloaded")
            unencryptedFileName = os.path.splitext(fileName)[0]
            pyAesCrypt.decryptFile(fileName, unencryptedFileName,dencryptionKey, bufferSize)
            os.system("mv " + unencryptedFileName + " /home/" + getpass.getuser() + "/Downloads")
            print("File Decrypted And Sent To Downloads Folder")
            null = input("Press ENTER To Return To Main Menu")
            mainFunction()
        os.system("rm " + fileName)
        dencryptionKey = ''
        c.close()
        longLine()
        print("File Has Been Downloaded")
        null = input("Press Enter To Return To Main Menu")
        mainFunction()

#Adds A Key File To Session
def addKeyScreen():
    title()
    global keyFile
    keyFile = input("Key To Add: ")
    exists = os.path.isfile(keyFile)  #Check To See If Key File Exists
    if (exists):
        longLine()
        print("Key Added Successfully")
        null = input("Press ENTER To Continue")
        mainFunction()
    else:
        keyFile = ''
        print("Key File Not Found")
        null = input("Press ENTER To Return To Main Menu")
        mainFunction()

#Removes Key From Session
def removeKeyScreen():
    title()
    global keyToDencrypt
    keyToDencrypt = ''
    print("Successfully Removed Key")
    null = input("Press ENTER To Continue")
    main()

#Generates Key File With Bit Number Argument
def keyGenScreen(bits):
    title()
    keyFileName = input("Key File Name: ") + ".dnckey" #Generates String With Key File Name (.dnckey extension)
    longLine()
    print("Generating A " + str(bits) + " Bit Key...")
    longLine()
    key = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(bits)) #Generates The Key
    for c in key:   #Slowly Prints Out The Key
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.1)
    print('')   #Acts Like /n And Returns To New Line
    longLine()
    with open(keyFileName, 'w+') as keyFileObject:   #Create Key File In Write Mode
        keyFileObject.write(key)    #Write Key To File
    print("Saving To " + keyFileName)
    time.sleep(0.3)
    print("Done")
    longLine()
    print("###DO NOT SHARE THIS KEY UNLESS YOU TRUST THEM###")
    longLine()
    useKey = input("Use This Key To Encrypt Files? [yes/no]: ")
    if (useKey.lower() == "yes"):   #If User Wants To Add Key To Session Add The Key.
        global keyFile
        keyFile = keyFileName
    null = input("Press ENTER to Continue")
    mainFunction()

#Encrypts Fiile The User Inputs
def encryptScreen():
    title()
    unencryptedFileName = input("File To Encrypt: ")
    longLine()
    print("Using " + keyFile + " as Key For Encryption")
    print("Encrypting File...")
    longLine()
    time.sleep(1)
    encryptedFileName = unencryptedFileName + ".dnc"
    pyAesCrypt.encryptFile(unencryptedFileName, encryptedFileName, dencryptionKey, bufferSize)    #Encrypts File With Key
    print("Your File Has Been Encrypted")
    null = input("Press ENTER to Continue")
    mainFunction()

#Decrypts File The User Inputs
def decryptScreen():
    title()
    encryptedFileName = input("File To Decrypt: ")
    longLine()
    print("Using " + keyFile + " as Key For Decryption")
    print("Decrypting File...")
    longLine()
    time.sleep(1)
    unencryptedFileName = os.path.splitext(encryptedFileName)[0]
    pyAesCrypt.decryptFile(encryptedFileName, unencryptedFileName,dencryptionKey, bufferSize)  #Decrypts File With Key; If Wrong Key Is Given, File Will Still Decrypt But Data Is Still Garbled
    print("Your File Has Been Decrypted")
    null = input("Press ENTER to Continue")
    mainFunction()

#Encrypts Folder Contents
def encryptFolderScreen():
    title()
    folderToEncrypt = input("Folder To Encrypt: ")
    longLine()
    print("Using " + keyFile + " as Key For Encryption")
    print("Encrypting Files")
    longLine()
    for file in os.listdir(folderToEncrypt):    #Gets Filenames In The Folder
        print(file + "              OK")
        encryptedFileName = file + ".dnc"
        pyAesCrypt.encryptFile(file, encryptedFileName, dencryptionKey, bufferSize)   #Encrypts Each File With Session Key
        time.sleep(0.1)
    longLine()
    print("All Files Have Been Encrypted")
    null = input("Press ENTER To Return To Main Menu")
    mainFunction()

#Decrypts Folder Contents
def decryptFolderScreen():
    title()
    folderToDecrypt = input("Folder To Decrypt: ")
    longLine()
    print("Using " + keyfile + " as Key For Decryption")
    print("Decrypting Files")
    longLine()
    for file in os.listdir(folderToDecrypt):    #Gets File Names In Folder
        print(file + "              OK")
        decryptedFileName = os.path.splitext(File)[0]
        pyAesCrypt.decryptFile(file, decryptedFileName, dencryptionKey, bufferSize)   #Decrypts Each File
        time.sleep(0.1)
    longLine()
    print("All Files Have Been Decrypted")
    null = input("Press ENTER To Continue")
    mainFunction()

def kBInterrupt():
    title()
    print("A Keyboard Interrupt Was Detected")
    print("Encryption/Decryption Progress Has Been Lost")
    returnToMain = input("Return To Main Menu? [yes/no]: ")
    if (returnToMain.lower() == "yes"):
        mainFunction()
    elif (returnToMain == "no"):
        clear()
        exit()
    else:
        kBInterrupt()

def mainFunction():
    try:
        main()
    except KeyboardInterrupt:   #Detect A Key Board Intterupt (CTRL-C)
        kBInterrupt()

#Run Main Function
#From Here Main Function Jumps To Other Functions That Return To Other Functions
#The Program Is Essential Based Off Functions Using THem As Blocks Of Code To Execute
mainFunction()
