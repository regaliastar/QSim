const { ipcMain } = require('electron')
// const { program } = require('commander')
const { Command } = require('commander') // include commander in git clone of commander repo
const program = new Command()
const { exec } = require('child_process')
const package = require('../package.json')

ipcMain.on('asynchronous-message', (event, arg) => {
  event.sender.send('asynchronous-reply', 'pong')
})

ipcMain.on('shell-input', (event, arg) => {
  const argv = arg.split(' ')
  if (argv[0] === 'qsim') {
    argv.shift()
    try {
      program.exitOverride()

      program
        .version(package.version, '-v', '-V', '--version')
        .option('-h, --help', 'help information')
        .option('-d, --debug', 'debug source code')
        .option('-q, --quit', 'quit program')
        .option('-s, --save', 'save code from textarea')
        .option('-l, --lexer', 'generate lexer token')
        .option('-p, --parser', 'generate AST(Abstract syntax tree)')
        .option('-tpy, --transpy', 'translate QLight to python')

      program.parseAsync(argv, { from: 'user' })

      if(program.help){
        event.sender.send('shell-reply', program.helpInformation())
        console.log('program.help!')
      }

      if (program.quit) {
        event.sender.send('shell-reply', 'quit')
        console.log('quit!')
      }
      if (program.save) {
        event.sender.send('shell-reply', 'save')
        console.log('save!')
      }
      if (program.lexer) {
        event.sender.send('shell-reply', 'lexer')
        console.log('lexer!')
      }
      if (program.parser) {
        event.sender.send('shell-reply', 'parser')
        console.log('parser!')
      }
      if (program.transpy) {
        event.sender.send('shell-reply', 'transpy')
        console.log('transpy')
      }
      event.sender.send('shell-reply', '')

    } catch (e) {
      console.log('Catch', e)
      event.sender.send('shell-reply', 'Catch:' + e.name)
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
