import sys

def usage():
    print "Wrapper for script to check PoGo API version and kill all python processes if it doesn't match local version.\nWill loop indefinitely, checking at specified intervals (default 3s).\n\nUsage: {} [-n,-t, -h]\n-n\tVersion to check against.\n-t\tCheck/loop interval (in seconds, decimals allowed)\n-h\tThis help text.".format(sys.argv[0])
    sys.exit(0)

 #Make sure they gave us a number
def validate_interval_input(input):
    try:
        return float(input)
    except ValueError:
         print "Invalid interval value: {}\nExiting.".format(input)
         sys.exit(1)
        

if __name__ == "__main__":

    import getopt
    import pogo_api_check as pac
    import datetime
    import time
    import logging
    
    start_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    
    logging.basicConfig(filename="pac_scheduler_{}.log".format(start_time), level=logging.WARNING)
    
    #This represents the local version of the API
    my_ver = "0.53.0"
    
    #How long to wait (in seconds) between checks
    interval = 0.5
    
    args, opts = getopt.getopt(sys.argv[1:], "n:t:h")
    
    for arg in args:
        if arg[0] == "-n":
            my_ver = arg[1]
        elif arg[0] == "-t":
            interval = validate_interval_input(arg[1])
        elif arg[0] == "-h":
            usage()
        else:
            usage()
    try:
        #import bob
        #Loop forever
        while(True):
            cur_time = datetime.datetime.now()
            formatted_cur_time = cur_time.strftime("%Y%m%d%H%M%S")
            cur_ver = pac.get_current_version()
            
            if (cur_ver != my_ver):
                #That's a bingo! Add log entry and kill all human- er, I mean python processes...
                logging.warning("{0}: Version mismatch (local: {1}, Niantic's: {2})".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S"), my_ver, cur_ver))
                pac.kill_python()
            
            #Do nothing until the next interval
            time.sleep(interval - time.time() % interval)
    except KeyboardInterrupt:
        #Someone pressed ctrl-c, or something equally annoying.
        logging.error("{0}: Process execution interrupted by user (KeyboardInterrupt). Exiting.".format(formatted_cur_time))
        sys.exit(1)
    except ValueError as e:
        logging.error("{0}: Unexpected return value: {1}.\nExiting.".format(formatted_cur_time, e))
        sys.exit(1)
    except Exception as e:
        logging.error("{0}: Unexpected error: {1}.\nExiting.".format(formatted_cur_time, e))
        sys.exit(1)