const { ipcMain } = require('electron')
const { exec } = require('child_process')

ipcMain.on('shell-input', (event, arg) => {
  exec(arg, { timeout: 3000, encoding: 'utf8' }, (err, stdout, stderr) => {
    if (err) {
      if (err.killSignal == 'SIGTERM') {
        event.sender.send('shell-reply', 'timeout err!')
      } else {
        event.sender.send('shell-reply', err)
      }
      return
    }
    if (stdout) {
      event.sender.send('shell-reply', stdout)
    }
    if (stderr) {
      event.sender.send('shell-reply', stderr)
    }
  })
})
