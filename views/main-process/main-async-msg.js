const {ipcMain} = require('electron')
const { program } = require('commander')

ipcMain.on('asynchronous-message', (event, arg) => {
  event.sender.send('asynchronous-reply', 'pong')
})

ipcMain.on('shell-input', (event, arg) => {
  arg.split(' ')
  program
    .option('-h', '--help', 'request help')
    .version('1.0.0')
    .parse(arg)
  if(program.help){
    console.log('there is help!')
  }

  event.sender.send('shell-reply', arg)

})