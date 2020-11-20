const { ipcMain } = require('electron')
const { Sheller } = require('./Sheller')
const { exec } = require('child_process')
const package = require('../package.json')

ipcMain.on('asynchronous-message', (event, arg) => {
  event.sender.send('asynchronous-reply', 'pong')
})

ipcMain.on('shell-input', (event, arg) => {
  const argv = arg.split(' ')
  if (argv[0] === 'qsim') {
    try {
      const sheller = new Sheller()
      sheller
        .version(package.version)
        .name('QSim')
        .usage('[options]')
        .setCmdHeader('qsim')
        .option('-v', 'version info', () => {
          event.sender.send('shell-reply', sheller.v)
        })
        .option('-h', 'help information', () => {
          event.sender.send('shell-reply', sheller.helpInformation())
        })
        .option('-d', 'debug source code', () => {
          event.sender.send('shell-reply', 'debug source code')
        })
        .option('-q', 'quit program', () => {
          event.sender.send('shell-reply', 'quit program')
        })
        .option('-s', 'save code from textarea', () => {
          event.sender.send('shell-reply', 'save code from textarea')
        })
        .option('-l', 'generate lexer token', () => {
          event.sender.send('shell-reply', 'generate lexer token')
        })
        .option('-p', 'generate AST(Abstract syntax tree)', () => {
          event.sender.send('shell-reply', 'generate AST(Abstract syntax tree)')
        })
        .option('-tpy', 'translate QLight to python', () => {
          event.sender.send('shell-reply', 'translate QLight to python')
        })

        sheller.parse(argv.join(' '), { from: 'user' })

    } catch (e) {
      console.log('Catch', e)
      event.sender.send('shell-reply', 'Catch:' + e)
    }
  } else {

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
  }
})
