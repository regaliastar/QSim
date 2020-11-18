const {ipcRenderer} = require('electron')

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

shellInput.addEventListener('keydown', e => {
  if(e.keyCode == '13'){
    const msg = shellInput.value,
    node = document.createElement("SPAN"),
    textnode = document.createTextNode('$ '+msg);
    shellInput.value = ''
    node.appendChild(textnode)
    document.getElementById('shell-msg').appendChild(node)
    ipcRenderer.send('shell-input', msg)
  }
})

ipcRenderer.on('shell-reply', (event, arg) => {
  const message = `shell: ${arg}`,
  node = document.createElement("P"),
	textnode = document.createTextNode(message);
	node.appendChild(textnode)
  document.getElementById('shell-msg').appendChild(node)
})