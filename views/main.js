const { app, BrowserWindow } = require('electron')
const path = require('path')
const glob = require('glob')

let pyProc = null
let pyPort = null

// create python process
const createPyProc = () => {
  let port = '4242'
  let script = path.join(__dirname,'..', 'service', 'service.py')
  pyProc = require('child_process').spawn('python', [script, port])
  if (pyProc != null) {
    console.log('child process success')
  }
}

// quit python process
const exitPyProc = () => {
  pyProc.kill()
  pyProc = null
  pyPort = null
}


function createWindow() {
  const win = new BrowserWindow({
    width: 1000,
    height: 600,
    webPreferences: {
      nodeIntegration: true
    }
  })

  win.loadFile('index.html')
  // win.webContents.openDevTools()
}

function initialize() {
  loadDemos()

  app.whenReady().then(createWindow)

  app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
      app.quit()
    }
  })

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })

  app.on('ready', createPyProc)
  app.on('will-quit', exitPyProc)
}

// Require each JS file in the main-process dir
function loadDemos() {
  const files = glob.sync(path.join(__dirname, 'main-process/*.js'))
  files.forEach((file) => { require(file) })
}

initialize()