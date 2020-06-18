#Python METAR decoder, for use in a conky
#requires curl and the metar package

from metar import Metar
import subprocess
import sys
import os

#define the usage function
def usage():
    program = os.path.basename(sys.argv[0])
    print("Usage:", program, "Site")
    print("""This program fetches a METAR report from Site, and then uses the metar
    python package to decode said report.""")
    sys.exit(1)

site = []
if sys.argv[1] == "-h":
    usage()
else:
    site.append(sys.argv[1])

for name in site:
    #We need to fetch the METAR file. We can't send the output to a file,
    #as conky will not be able to use it properly.
    #see https://stackoverflow.com/questions/11958729/piping-file-contents-to-conky
    #So what we will do is iterate over the lines in the output of curl.
    rawreport = subprocess.Popen(["curl", "https://tgftp.nws.noaa.gov/data/observations/metar/stations/" + name + ".TXT","--silent"],stdout=subprocess.PIPE)
    try:
        if not rawreport:
            print("No data for ", name, "\n\n")
        else:
            while True:
                line = rawreport.stdout.readline()
                #strip new line characters
                line = line.rstrip()
                #we need to decode the line, line is a bytes string literal
                decodedline = line.decode('utf-8')
                print(decodedline)
                if decodedline.startswith(name):
                    report = decodedline.strip()
                    obs = Metar.Metar(decodedline)
                    print(obs.string())
                    break
    except Metar.ParserError as exc:
        print("METAR code: ", decodedline)
        print(string.join(exc.args, ", "), "\n")
    except:
        import traceback
        print(traceback.format_exc())
        print("Error retrieving", name, "data", "\n")
