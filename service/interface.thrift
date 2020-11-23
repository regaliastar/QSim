/**
 * 定义接口文件
 * render-async-msg.js:
 *  客户端通过JSON.stringify传输json格式数据 
 * service.py:
 *  服务端解析json，并返回json.dumps处理后的字符串
 *
 * 编写该文件后执行gen.sh可生成py&nodejs可调用的interface代码
 */
service userService {
    string load(1:string code)
}