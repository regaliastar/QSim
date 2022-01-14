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

const { ipcRenderer, remote } = require('electron')
const { dialog, Menu } = remote
const _package = require('../package.json')
const thrift = require('thrift')
const userService = require('../gen-nodejs/userService.js')
const { Sheller } = require('./Sheller')

const thriftConnection = thrift.createConnection(_connect.ip, _connect.port, {
  connect_timeout: _connect.connect_timeout,
  max_attempts: _connect.max_attempts
})
const thriftClient = thrift.createClient(userService,thriftConnection)
thriftConnection.on("error", e =>{
  console.error(e)
  alert(e)
})

document.getElementById('version').innerHTML = 'v'+_package.version


/**
 * Sheller
 */
function parseShell(arg){
  console.log('parseShell', arg)
  const argv = arg.split(' ')
  if (argv[0] === 'qsim') {
    try {
      const sheller = new Sheller()
      sheller
        .version(_package.version)
        .name('QSim')
        .usage('[options]')
        .setCmdHeader('qsim')
        .option('-v', 'version info', () => {
          printInShell(sheller.v)
        })
        .option('-h', 'help information', () => {
          printInShell(sheller.helpInformation())
        })
        .option('-d', 'debug source code', () => {
          debug()   
        })
        .option('-q', 'quit program', () => {
          console.log('quit')
        })
        .option('-s', 'save code from textarea', () => {
          save_code()  
        })
        .option('-l', 'generate lexer token', () => {
          const route = 'le'
          const source_code = document.getElementById('playground-input').value.trim()
          const json = {
            source_code,
            route
          }
          thriftClient.load(JSON.stringify(json), (error, res) => {
            console.log('lexer-reply', res)
            if (error) {
              console.error(error)
              printInShell(error, {type: 'error'})
            } else {
              const message = JSON.parse(res)
              if(message.MessageType == 'error'){
                printInShell(message.info, {type: message.MessageType})
                return
              }
              printInShell(message.info, {type: message.MessageType})
            }
          })
        })
        .option('-tpy', 'translate QLight to python', () => {
          const route = 'tpy'
          const source_code = document.getElementById('playground-input').value.trim()
          const json = {
            source_code,
            route
          }
          thriftClient.load(JSON.stringify(json), (error, res) => {
            console.log('tpy-reply', res)
            if (error) {
              console.error(error)
              printInShell(error, {type: 'error'})
            } else {
              const message = JSON.parse(res)
              if(message.MessageType == 'error'){
                printInShell(message.info, {type: message.MessageType})
                return
              }
              printInShell(message.info, {type: message.MessageType})
            }
          })   
        })
        .option('-tqasm', 'translate QLight to QASM', () => {

        })
        
      sheller.parse(argv.join(' '), { from: 'user' })
    } catch (e) {
      console.log('Catch', e)
      printInShell(e)
    }
  } else if (arg == 'clear'){
    const domEl = document.getElementById('shell-msg')
    while(domEl.lastChild){
      domEl.removeChild(domEl.lastChild)
    }
  } else {
    ipcRenderer.send('shell-input', arg)
  }
}


/**
 * debug处理部分
 */
function debug(){
  const txt_code = document.getElementById('playground-input').value.trim()
  const source_code = PreScanner(txt_code.trim())
  const route = 'debug'
  const json = {
    _filepath,
    _algo,
    source_code,
    route
  }
  thriftClient.load(JSON.stringify(json), (error, res) => {
    if (error) {
      console.error(error)
      printInShell(error, {type: 'error'})
    } else {
      // console.log('thriftClient.load', res)
      const message = JSON.parse(res)
      console.log('message', typeof message, message)
      if(message.MessageType == 'error'){
        printInShell(message.info, {type: message.MessageType})
        return
      }

      /**
       * output 由 show 字段与 wave_func 字段构成
       * 当存在 show 时候，只输出 show
       */
      let output = `simulation_env: false\n`
      if (message.show.length > 0) {
        output += 'result: \n'
        for(let i = 0; i < message.show.length; i++){
          output += message.show[i] + '\n'
        }
      } else {
        output += message.wave_func
      }
      output += `\ncost time:  ${message.t_cost} S`
      output += `\nmemory:  ${message.memory_cost} MB`
      printInShell(output, {type: message.MessageType})
    }
  })
}
document.getElementById('playground-apply-button').addEventListener('click', debug)


/**
 * shell处理部分
 */

function printInShell(msg, opt){
  // 将信息打印到terminal
  const node = document.createElement("P")
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
      node = document.createElement("P"),
      textnode = document.createTextNode('$ ' + msg);
    inputHistory.push(msg)
    inputHistoryPtr = inputHistory.length - 1
    // 清空输入框
    shellInput.value = ''
    
    node.appendChild(textnode)
    document.getElementById('shell-msg').appendChild(node)
    parseShell(msg)
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

/**
 * save-button
 */
function save_code(){
  const source_code = document.getElementById('playground-input').value.trim()
  let filename = dialog.showSaveDialog({
    title: 'save code',
    filters: [
      { name: 'log', extensions: ['log', 'txt', '*'] }
    ]
  }).then(result => {
    filename = result.filePath
    if (filename === undefined) {
      alert('the user clicked the btn but didn\'t created a file')
      return
    }
    fs.writeFile(filename, source_code, (err) => {
      if (err) {
        console.error('an error ocurred with file creation ' + err.message)
        return
      }
    })
  }).catch(err => {
    alert(err)
  })
  console.log(filename)
}
document.getElementById('save-button').addEventListener('click', save_code)

/**
 * 右键创建菜单
 */
const createContextMenu = () => {
  const contextTemplate = [
    {
      label: 'Reload',
      role: 'reload'
    },
    {
      label: 'Cut',
      role: 'cut'
    },
    {
      label: 'Copy',
      role: 'copy'
    },
    {
      label: 'Paste',
      role: 'paste'
    }
  ]
  const contextMenu = Menu.buildFromTemplate(contextTemplate)
  return contextMenu
}

window.addEventListener('contextmenu', (event) => {
  event.preventDefault()
  const contextMenu = createContextMenu();
  contextMenu.popup({
    window: remote.getCurrentWindow()
  })
}, false)
