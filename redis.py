import os
import random
import argparse
import linecache
class configlist:
    def __init__(self,path,config):
        self.path=path
        self.config=config
def endwith(dir_path,filters):
    for cur_dir, sub_dir, files in os.walk(dir_path):
        for file in files:
            #print(os.path.splitext(file)[1])
            if os.path.splitext(file)[1] == filters:
                config=""
                file_abs_path = os.path.join(cur_dir, file)
                print(file_abs_path)
                print(file)
                config=readconfig(file_abs_path)

                l1=configlist(file_abs_path,config)
                #print(l1.path)
                #print(l1.config)
def readconfig(filepath):

    with open(filepath) as lines:

        data=lines.readline()
        config=""
        while data:
            if data.find('#')==-1:
                #print(data,end=' ')

                if data.split():
                    config=config+data
            data=lines.readline()
    return config
    #print(config)
def run(cmd_str='./redis-server -h',echo_print=1):
    import subprocess
    if echo_print==1:
        print('执行cmd命令=“{}'.format(cmd_str))
        return subprocess.Popen(cmd_str,shell=True)


def run1(cmd_str='redis-server', echo_print=1):
    import subprocess
    cmd_str = "./" + cmd_str + " -h full" \
                               ""
    if echo_print == 1:
        print('执行cmd命令=“{}'.format(cmd_str))
        return subprocess.Popen(cmd_str, shell=True)


if __name__=='__main__':
    parser = argparse.ArgumentParser(prog='config find', description="to find the config can be change")
    parser.add_argument('-d',dest='dir',type=str,action='store',help='the path you want to run')
    args=parser.parse_args()
    if args.dir:
        run(args.dir)
    div=os.getcwd();
    f_file=[]
    lis = {}

    #endwith(div,'.conf')
    i=0
    for cur_dir, sub_dir, files in os.walk(div):


        for file in files:

            #print(os.path.splitext(file)[1])
            if os.path.splitext(file)[1] == '.conf':
                print(file)

                file_abs_path = os.path.join(cur_dir, file)
                #print(file_abs_path)
                config=readconfig(file_abs_path)

                lis[i]=configlist(file_abs_path,config)
                #print(file)
                #print(l[i].path)
                #print(lis[i].config)

                i=i+1
                #print(i)

    for m in range(10):
        a=random.randint(0,i-1)
        data=lis[a].config
        with open("1.txt",'w') as f:
            f.write(data)
        count = len(open("1.txt", 'r').readlines())
        #print(count)
        b=random.randint(0,count)
        c=linecache.getline('1.txt', b)
        #print(c)
        cmd="./src/redis-server"+' '+lis[a].path+' --'+c
        #print(cmd)
        os.remove("1.txt")
        with open("2.txt",'a') as f1:
            f1.write(cmd)
