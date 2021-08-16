import datetime
import os, re, sys

def onlyFacts(directoryName):
    curdir = directoryName
    dirname = os.path.basename(curdir)
    parentdir = os.path.abspath(os.path.join(curdir, os.pardir))

    #now_time = datetime.datetime.now()
    #now_time_str = "-".join(str(now_time).split(" ")).replace(":", "-").replace(".", "")

    fact_file_path = parentdir + '/' + 'Fact_' + dirname
    os.mkdir(fact_file_path)


    for fili in os.listdir(curdir):
        print(fili)
        if fili.endswith(".tsv"):
            with open(curdir+"/"+fili, "r") as tsfctfile:
                with open(fact_file_path +"/"+ fili, "w") as ftsfctfile:
                    for i in tsfctfile.readlines():
                        i1 = re.search(r"(^.*)\[text\]",i).group(1)
                        i2 = re.search(r"\[text\].*\[/text\]",i).group()
                        to_write_beta = " ".join(
                            re.findall(r"\[__FACT.*?__ARG1.*?__ARG2.*?\].*?\]", i1, re.IGNORECASE) + re.findall(r"\[__OPTIONAL.*\]", i1, re.IGNORECASE)) + "\t"+ i2
                        #to_write_alpha = ' '.join(to_write_beta.split())
                        #to_write_final = re.sub(r"\t+", "\t", to_write_alpha)
                        ftsfctfile.write(to_write_beta +"\n")


if __name__ == "__main__":
    onlyFacts(str(sys.argv[1]))
    print('creating Fact for'+str(sys.argv[1]))
