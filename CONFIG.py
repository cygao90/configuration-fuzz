import re
import os
import argparse
def endwith(dir_path,filters):
    for cur_dir, sub_dir, files in os.walk(dir_path):
        for file in files:
            #print(os.path.splitext(file)[1])
            if os.path.splitext(file)[1] == filters:

                file_abs_path = os.path.join(cur_dir, file)
                print(file_abs_path)
                readconfig(file_abs_path)

def readconfig(filepath):
    with open(filepath) as lines:
        config=""
        data=lines.readline()
        while data:
            if data.find('#')==-1:
                #print(data,end=' ')
                if data.split():
                    config=config+data
            data=lines.readline()

    print(config)
def run(cmd_str='./redis-server -h',echo_print=1):
    import subprocess
    if echo_print==1:
        print('执行cmd命令=“{}'.format(cmd_str))
        return subprocess.Popen(cmd_str,shell=True)


def run(cmd_str='redis-server', echo_print=1):
    import subprocess
    cmd_str = "./" + cmd_str + " -h"
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
    endwith(div,'.conf')