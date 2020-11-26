########### Introduction ############
# 需要将thrift.exe放在当前文件夹下再执行 !important
# 在编写 interface.thrift 后执行
# 根据 interface.thrift 直接生成py&nodejs可调用的代码
# 每次修改 interface.thrift 后都需要执行该文件
# 需要将生成的文件转移目录 !important

# -out 调整输出文件的目录

# py，在当前目录生成gen-py文件夹
./thrift -gen py interface.thrift

# js:node，在当前目录生成gen-nodejs文件夹
./thrift -gen js:node interface.thrift
