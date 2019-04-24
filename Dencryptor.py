#Dencryptor: Encryption And Decryption Software
#Encryption: AES
#UI: Terminal Interface
#Dependencies:  Python{Pycrypto}, System{figlet}
#Created By: BaconBombz
#Version 2.0

###VERSION INFO###
#Version 1.0 Offers Basic Encryption And Decryption
#Version 2.0 Offers Secure File Transfer Over The Internet

#Import Neccessary Libraries
import os, random, struct, string, time, sys, readline, socket
from Crypto.Cipher import AES

#Global Variables Initialization
keyToDencrypt = ''  #Key File
dencryptionKey = '' #Key File Contents
port = 41235

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
    if (len(keyToDencrypt) > 0):
        print("Key: " + keyToDencrypt)
        dencryptionKeyFile = open(keyToDencrypt, 'r')
        dencryptionKey = dencryptionKeyFile.read()
        longLine()
    print("1) Encrypt A File")
    print("2) Decrypt A File")
    print("3) Encrypt A Folder")
    print("4) Decrypt A Folder")
    print("5) Send A Secure File Transfer")
    print("6) Recieve A Secure File Transfer")
    print("7) Generate A 16 Bit Key")
    print("8) Generate A 24 Bit Key")
    print("9) Generate A 32 Bit Key")
    print("10) Add Key To Session")
    print("11) Remove Key From Session")
    print("0) Exit")
    longLine()
    option = raw_input("Option: ")
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
        keyGenScreen(24)    #Generates A 24 Bit Key File
    elif (option == "9"):
        keyGenScreen(32)    #Generates A 32 Bit Key File
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
    rHost = raw_input("Reciever's IP: ")
    fileToSend = raw_input("File To Send: ")
    longLine()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((rHost, port))
        sendConfirm = s.recv(1)
        if (sendConfirm == '1'):
            encryptedFile = fileToSend + ".dnc"
            print("Encrypting File...")
            encrypt(dencryptionKey, fileToSend)
            time.sleep(1)
            longLine()
            print("Sending File Name")
            longLine()
            s.send(encryptedFile)
            time.sleep(1)
            print("Sending Key...")
            time.sleep(1)
            s.send(dencryptionKey)
            longLine()
            print("Sending File...")
            time.sleep(1)
            encryptedFileOpen = open(encryptedFile, "r")
            s.send(encryptedFileOpen.read())
            encryptedFileOpen.close()
            os.system("rm " + encryptedFile)
        elif (sendConfirm == 0):
            s.close()
            print("Reciever Rejected The Connection")
            null = raw_input("Press ENTER To Return To Return To The Main Menu")
            mainFunction()
    except socket.error:
        s.close()
        print("There Was An Error Connecting To The Reciever")
        null = raw_input("Press ENTER To Return To Return To The Main Menu")
        mainFunction()

def recieveFileScreen():
    title()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", port))
    s.listen(120)
    c, addr = s.accept()
    print(str(addr) + " Wants To Send A File...")
    confirm = raw_input("Would You Like To Recieve The File? [yes/no]: ")
    if (confirm.lower() == "yes"):
        c.send('1')
        longLine()
        print("Getting File Name")
        fileName = c.recv(16)
        print("File Name: " + fileName)
        longLine()
        time.sleep(0.3)
        print("Recieving Key")
        longLine()
        time.sleep(0.3)
        global dencryptionKey
        dencryptionKey = c.recv(32)
        print("Key Recieved")
        longLine()
        time.sleep(0.3)
        print("Recieving File")
        longLine()
        time.sleep(0.3)
        encryptedFile = c.recv(64000)
        encryptedFileOpen = open(fileName, "w+")
        encryptedFileOpen.write(encryptedFile)
        encryptedFileOpen.close()
        decrypt(dencryptionKey, fileName)
        os.system("rm " + fileName)
        dencryptionKey = ''
        c.close()

#Adds A Key File To Session
def addKeyScreen():
    title()
    global keyToDencrypt
    keyToDencrypt = raw_input("Key To Add: ")
    exists = os.path.isfile(keyToDencrypt)  #Check To See If Key File Exists
    if (exists):
        keyFile = open(keyToDencrypt, "r")
        keyBits = len(keyFile.read())
        keyFile.close
        bits = {16,24,32}
        if(keyBits in bits):
            print("Key Added Successfully")
            null = raw_input("Press ENTER To Continue")
            main()
        else:
            print("Key Is Not 16, 24, Or 32 Bits")
            keyToDencrypt = ''
            null = raw_input("Press ENTER To Retry")
            addKeyScreen()
    else:
        keyToDencrypt = ''
        print("Key File Not Found")
        null = raw_input("Press ENTER To Retry")
        addKeyScreen()

#Removes Key From Session
def removeKeyScreen():
    title()
    global keyToDencrypt
    keyToDencrypt = ''
    print("Successfully Removed Key")
    null = raw_input("Press ENTER To Continue")
    main()

#Generates Key File With Bit Number Argument
def keyGenScreen(bits):
    title()
    keyName = raw_input("Key File Name: ") + ".dnckey" #Generates String With Key File Name (.dnckey extension)
    print("Generating A " + str(bits) + " Bit Key...")
    longLine()
    key = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(bits)) #Generates The Key
    for c in key:   #Slowly Prints Out The Key
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.2)
    print('')   #Acts Like /n And Returns To New Line
    longLine()
    keyFile = open(keyName, 'w+')   #Create Key File In Write Mode
    print("Saving To " + keyName)
    keyFile.write(key)  #Write Key To File
    keyFile.close()
    time.sleep(0.3)
    print("Done")
    print("###DO NOT SHARE THIS KEY UNLESS YOU TRUST THEM###")
    useKey = raw_input("Use This Key To Encrypt Files? [yes/no]: ")
    if (useKey.lower() == "yes"):   #If User Wants To Add Key To Session Add The Key.
        global keyToDencrypt
        keyToDencrypt = keyName
    null = raw_input("Press ENTER to Continue")
    main()

#Encrypts Fiile The User Inputs
def encryptScreen():
    title()
    unencryptedFile = raw_input("File To Encrypt: ")
    longLine()
    print("Using " + keyToDencrypt + " as Key For Encryption")
    print("Encrypting File...")
    time.sleep(1)
    encrypt(dencryptionKey, unencryptedFile)    #Encrypts File With Key
    longLine()
    print("Your File Has Been Encrypted")
    null = raw_input("Press ENTER to Continue")
    main()

#Decrypts File The User Inputs
def decryptScreen():
    title()
    encryptedFile = raw_input("File To Decrypt: ")
    longLine()
    print("Using " + keyToDencrypt + " as Key For Decryption")
    print("Decrypting File...")
    time.sleep(1)
    decrypt(dencryptionKey, encryptedFile)  #Decrypts File With Key; If Wrong Key Is Given, File Will Still Decrypt But Data Is Still Garbled
    time.sleep(0.05)
    longLine()
    print("Your File Has Been Decrypted")
    null = raw_input("Press ENTER to Continue")
    main()

#Main Handler For Encrypting Files
def encrypt(key, unencryptedFile, encryptedFile=None, chunkSize=64*1024):
    if not encryptedFile:
        encryptedFile = unencryptedFile + ".dnc"    #Encrypted File Name

        initVector = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))   #Generate An AES IV
        encryptor = AES.new(key, AES.MODE_CBC, initVector)  #Create Encryptor Object
        fileSize = os.path.getsize(unencryptedFile) #Get File Size Of File To Encrypt

        unencryptedFileOpen = open(unencryptedFile, 'rb')   #open Unencrypted File In Read Mode
        encryptedFileOpen = open(encryptedFile, "wb")   #Creates Encrypted File In Write Mode

        encryptedFileOpen.write(struct.pack('<Q', fileSize))    #Writes Packed File Size To Encrypted File
        encryptedFileOpen.write(initVector) #Writes AES IV To Encrypted File

        while (True):
            chunk = unencryptedFileOpen.read(chunkSize)

            if (len(chunk) == 0):
                break
            elif (len(chunk) % 16 != 0):
                chunk += ' ' * (16 - len(chunk) % 16)   #Pad The Chunk With Spaces To Fit AES Standard

            encryptedFileOpen.write(encryptor.encrypt(chunk))   #Write Chunk Into Encrypted File

#Main Handler For Decrypting Files
def decrypt(key, encryptedFile, decryptedFile=None, chunkSize=24*1024):
    if not decryptedFile:
        decryptedFile = os.path.splitext(encryptedFile)[0]  #Removes ".dnc" Extension

    encryptedFileOpen = open(encryptedFile, "rb")   #Opens Encrypted File In Read Mode
    decryptedFileOpen = open(decryptedFile, "wb")   #Creates Unencrypted FIle In Write Mode

    originalSize = struct.unpack('<Q', encryptedFileOpen.read(struct.calcsize('Q')))[0] #Calculates Original Size
    initVector = encryptedFileOpen.read(16) #Read The AES IV From Encrypted File
    decryptor = AES.new(key, AES.MODE_CBC, initVector)  #Creates Object For Decryption

    while True:
        chunk = encryptedFileOpen.read(chunkSize)   #Read Chunk
        if len(chunk) == 0:
            break
        decryptedFileOpen.write(decryptor.decrypt(chunk))   #Decrypt Chunk

    decryptedFileOpen.truncate(originalSize)    #Takes All Chunks And Puts Them Together

#Encrypts Folder Contents
def encryptFolderScreen():
    if (len(keyToDencrypt) > 0):
        title()
        folderToEncrypt = raw_input("Folder To Encrypt: ")
        longLine()
        print("Using " + keyToDencrypt + " as Key For Encryption")
        print("Encrypting Files")
        longLine()
        for file in os.listdir(folderToEncrypt):    #Gets Filenames In The Folder
            print(file + "  OK")
            encrypt(dencryptionKey, folderToEncrypt + "/" + file)   #Encrypts Each File With Session Key
            time.sleep(0.1)
        longLine()
        print("All Files Have Been Encrypted")
        null = raw_input("Press ENTER To Continue")
        main()
    else:
        title()
        print("Please Add An Encryption Key")
        null = raw_input("Press ENTER To Continue")
        main()

#Decrypts Folder Contents
def decryptFolderScreen():
    if (len(keyToDencrypt) > 0):
        title()
        folderToDecrypt = raw_input("Folder To Decrypt: ")
        longLine()
        print("Using " + keyToDencrypt + " as Key For Decryption")
        print("Decrypting Files")
        longLine()
        for file in os.listdir(folderToDecrypt):    #Gets File Names In Folder
            print(file + "  OK")
            decrypt(dencryptionKey, folderToDecrypt + "/" + file)   #Decrypts Each File
            time.sleep(0.1)
        longLine()
        print("All Files Have Been Decrypted")
        null = raw_input("Press ENTER To Continue")
        main()
    else:
        title()
        print("Please Add A Decryption Key")
        null = raw_input("Press ENTER To Continue")
        main()

def kBInterrupt():
    title()
    print("A Keyboard Interrupt Was Detected")
    print("Encryption/Decryption Progress Has Been Lost")
    returnToMain = raw_input("Return To Main Menu? [yes/no]: ")
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
