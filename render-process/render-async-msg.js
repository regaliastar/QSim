const path = require('path')
const YAML = require('yamljs')
const fs = require('fs')

 /**
  * 读取配置文件 _config.yml
  */
 const { 
  _filepath,
  _algo,
  _connect
} = YAML.parse(fs.readFileSync(path.join(__dirname,'..','_config.yml')).toString())

const { ipcRenderer } = require('electron')
const package = require('../package.json')
const thrift = require('thrift')
const userService = require('../gen-nodejs/userService.js')
const ttypes = require('../gen-nodejs/interface_types.js')
const thriftConnection = thrift.createConnection(_connect.ip, _connect.port, {
  connect_timeout: _connect.connect_timeout,
  max_attempts: _connect.max_attempts
})
const thriftClient = thrift.createClient(userService,thriftConnection)
thriftConnection.on("error", e =>{
    console.error(e)
    alert(e)
})

document.getElementById('version').innerHTML = 'v'+package.version

/**
 * debug处理部分
 */

const debugBtn = document.getElementById('playground-apply-button')

debugBtn.addEventListener('click', () => {
  const source_code = document.getElementById('playground-input').value.trim()
  const json = {
    _filepath,
    _algo,
    source_code
  }

  thriftClient.load(JSON.stringify(json), (error, res) => {
    if (error) {
      console.error(error)
      printInShell(error, {type: 'error'})
    } else {
      console.log('thriftClient.load', res)
      message = JSON.parse(res)
      if(message.MessageType == 'error'){
        printInShell(message.info, {type: message.MessageType})
        return
      }
      console.log('symbalTable', message.symbalTable)

      /**
       * output 由 show 字段与 wave_func 字段构成
       * 当存在 show 时候，只输出 show
       */
      let output = ''
      if (message.show.length > 0) {
        output += 'show: \n'
        for(let i = 0; i < message.show.length; i++){
          output += message.show[i] + '\n'
        }
      } else {
        output += message.wave_func

      }
      output += '\n执行时间: '+ message.t_cost
      printInShell(output, {type: message.MessageType})
    }
  })
})


/**
 * shell处理部分
 */

 function printInShell(msg, opt){
  // 将信息打印到terminal
  const message = `shell: ${msg}`,
    node = document.createElement("P");
  if(Object.prototype.toString.call(msg) === '[object Object]'){
    let seliMsg = ''
    for(let key in msg){
      seliMsg += key + ': \n'
      seliMsg += msg[key] + '\n'
    }
    const textnode = document.createTextNode(seliMsg);
    node.appendChild(textnode)
  }else{
    const textnode = document.createTextNode(msg);
    node.appendChild(textnode)
  }
  
  node.appendChild(document.createTextNode('\n----------------------------------------------'))
  node.style['white-space'] = 'pre-line'
  if(opt && opt.type == 'error')
    node.style['color'] = 'red'
  document.getElementById('shell-msg').appendChild(node)
 }

const shellInput = document.getElementById('shell-input')
const inputHistory = []
let inputHistoryPtr = 0

shellInput.addEventListener('keydown', e => {
  if (e.keyCode == '13') {
    const msg = shellInput.value,
      node = document.createElement("SPAN"),
      textnode = document.createTextNode('$ ' + msg);
    inputHistory.push(msg)
    inputHistoryPtr = inputHistory.length - 1
    // 清空输入框
    shellInput.value = ''
    
    node.appendChild(textnode)
    document.getElementById('shell-msg').appendChild(node)
    ipcRenderer.send('shell-input', msg)
  } else if (e.keyCode == '38') {
    shellInput.value = inputHistory[inputHistoryPtr]    
    shellInput.focus()
    if (inputHistoryPtr > 0) {
      inputHistoryPtr--
    }
  } else if (e.keyCode == '40') {
    if (inputHistoryPtr < inputHistory.length - 1) {
      inputHistoryPtr++
    }
    shellInput.value = inputHistory[inputHistoryPtr]
    shellInput.focus()
  }
})

ipcRenderer.on('shell-reply', (event, arg) => {
  printInShell(arg)
})