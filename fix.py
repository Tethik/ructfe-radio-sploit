with open("tokens.txt", "r") as fp:
    everything = fp.read() # fucked up and put everything on one single long line

parts = everything.split("http://")
with open("newtokens.txt", "w") as fp:
    for i, p in enumerate(parts):
        fp.write(p)
        fp.write("\n")
