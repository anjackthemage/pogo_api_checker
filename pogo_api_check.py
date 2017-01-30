import requests
import os
import sys
import re
import types


#Return the current PoGo API version from Niantic website.
def get_current_version():
    uri = "https://pgorelease.nianticlabs.com/plfe/version"
    result = requests.get(uri)
    if result.status_code == 200:
        parsed_result = re.findall('\d+\.\d+\.\d+', result.text)
        if (type(parsed_result) == types.ListType and parsed_result != []):
            return parsed_result #Remove formatting, just return the version number.
        else:
            raise ValueError("Received bad text from {0}: {1}\nParsed as: {2}".format(uri, result, parsed_result))
    else:
        raise ValueError("Received HTTP status code {0} from {1}.".format(result.status_code, uri))
        
#Kill all instances of python.exe (including this one)
def kill_python():
    result = os.system('taskkill /IM python.exe /f')
    #Below code is primarily for debugging.
    #If we get to this point, there was a problem.
    print result
    
def usage():
    print "Script to check PoGo API version and kill all python processes if it doesn't match local version.\n\nUsage: python.exe {} [-n, -h]\n-n\tVersion to check against.\n-h\tThis help text.".format(sys.argv[0])
    sys.exit(0)

if __name__ == "__main__":
    
    import getopt
    
    #This represents the local version
    my_ver = "0.53.0"
    #This represents the current version from Niantic
    cur_ver = ""
    
    args, opts = getopt.getopt(sys.argv[1:],"n:h")
    
    for arg in args:
        if arg[0] == "-n":
            my_ver = arg[1]
        elif arg[0] == "-h":
            usage()
    
    cur_ver = get_current_version()
    print "Your version: {0}\nNiantic version: {1}".format(my_ver, cur_ver)
    
    if (cur_ver != my_ver):
        print "Version mismatch! Killing all instances of python.exe."
        kill_python()
    else:
        print "Version match. Exiting."