const { ipcRenderer } = require('electron')
const package = require('../package.json')

document.getElementById('version').innerHTML = 'v'+package.version

const asyncMsgBtn = document.getElementById('playground-apply-button')

asyncMsgBtn.addEventListener('click', () => {
  ipcRenderer.send('asynchronous-message', 'ping')
})

ipcRenderer.on('asynchronous-reply', (event, arg) => {
  const message = `message reply: ${arg}`
  const node = document.createElement("P")
  const textnode = document.createTextNode(message);
  node.appendChild(textnode)
  document.getElementById('shell-msg').appendChild(node)
})

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
  const message = `shell: ${arg}`,
    // 将信息打印到terminal
    node = document.createElement("P"),
    textnode = document.createTextNode(message);
  node.appendChild(textnode)
  node.style['white-space'] = 'pre-line'
  document.getElementById('shell-msg').appendChild(node)
})