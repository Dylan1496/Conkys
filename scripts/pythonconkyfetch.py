#Python METAR decoder, for use in a conky
#requires curl and the metar package - https://github.com/python-metar/python-metar

from metar import Metar
import subprocess
import sys
import os

#define needed functions
def fetch_file(METAR_site):
    #fetches a METAR file. Takes a string as input, which must
    #be a valid METAR site. List can be found here:
    #https://tgftp.nws.noaa.gov/data/observations/metar/stations/
    #For example, Buffalo Niagara International is KBUF.
    subprocess.run(["curl", "https://tgftp.nws.noaa.gov/data/observations/metar/stations/" + METAR_site + ".TXT", "-o", "report.txt", "--silent"])

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
    fetch_file(name)
    rawreport = open('report.txt', 'r')
    try:
        for line in rawreport:
            
            if line.startswith(str(name)):
                report = line.strip()
                obs = Metar.Metar(line)
                print(obs.string())
                break
        if not rawreport:
            print("No data for ", name, "\n\n")
    except Metar.ParserErr as exc:
        print("METAR code: ", line)
        print(string.join(exc.args, ", "), "\n")
    except:
        import traceback
        
        print(traceback.format_exc())
        print("Error retrieving", name, "data", "\n")