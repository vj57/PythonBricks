#!/usr/bin/python
import re

class RouterIF:
    def __init__(self, output):
        self.output = output
        self.IFlist = {}

    def ReadLine(self):
        lines = self.output.splitlines()
        for index, line in enumerate(lines):
            if "Interface" in line:
                valuelist = []
                for i in [1,2,3]:
                    valuelist.append((lines[index+i].split(':'))[1].strip())
                self.IFlist[line.split()[1]] = valuelist
        return self.IFlist

    def IFaceWithDroppedPkt(self):
        DropIFace = []
        for key, values in self.IFlist.iteritems():
            print values
            print values[2]
            if values[2]>0:
                DropIFace.append(key)
        return DropIFace

    def readline3(self):
        gen_lines = (line for line in self.output.splitlines() if line and not line.isspace())
        print type(gen_lines)
        try:
            while True:
                start,_,key = next(gen_lines).partition(" ")
                if start == "Interface":
                    self.IFlist[key] = [next(gen_lines).rpartition(" : ")[2] for _ in "123"]
        except StopIteration:
            return self.IFlist

class RouterIFRegex:
    def __init__(self, output):
        self.output = output
        self.IFlist = {}

    def Readline(self):
     #print repr(self.output)
     n = re.compile(r"\n*Interface (./.)\n\s*input : ([0-9]+)\n\s*output : ([0-9]+)\n\s*dropped : ([0-9]+)",re.MULTILINE|re.DOTALL)
     blocks = self.output.split('\n\n')
     for block in blocks:
         m_object = re.match(n, block)
         self.IFlist[m_object.group(1)] = [m_object.group(i) for i in (2,3,4)]

    def IFaceWithDroppedPkt(self):
        DropIFace = []
        for key, values in self.IFlist.iteritems():
            print values
            print values[2]
            if values[2]>0:
                DropIFace.append(key)
        return DropIFace

if __name__ == '__main__':

    message = \
"""
Interface 1/1
    input : 1234
    output : 3456
    dropped : 12

Interface 1/2
    input : 7123
    output : 2345
    dropped : 31
"""
    flag = 1
    if flag == 1:
        obj = RouterIF(message)
        d_interface = obj.ReadLine()
        #print d_interface

        print obj.IFaceWithDroppedPkt()
        print "****"*10
        print obj.readline3()
        print "===="*10
    else:
        obj = RouterIFRegex(message)
        d = obj.Readline()
        print obj.IFaceWithDroppedPkt()

