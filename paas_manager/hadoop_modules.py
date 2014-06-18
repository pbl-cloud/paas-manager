import threading, subprocess

hostname = "star@192.168.122.10"

def start_hadoop(path, args, callback):
    command = ["ssh", hostname, "hadoop", "jar", path]
    command.extend(args)

    t = threading.Thread(target=exec_hadoop,args=(command, callback))
    t.setDaemon(True)
    t.start()
    return t

def exec_hadoop(command, callback):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    
    callback(bytes.decode(out), bytes.decode(err))
