import threading

def function(i):
    print ("function called by thread %i\n"  %i)
    return

threads = []
for i in range(10):
    t = threading.Thread(target=function , args=(i,))
    threads.append(t)
    t.start()
    #t.join() # to wait

