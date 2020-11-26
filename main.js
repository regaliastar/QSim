const { app, BrowserWindow } = require('electron')
const path = require('path')
const glob = require('glob')

let pyProc = null
let pyPort = null

// create python process
const PY_DIST_FOLDER = 'dist'
const PY_FOLDER = 'src'
const PY_MODULE = 'server' // without .py suffix

// have package：return True
const guessPackaged = () => {
  const fullPath = path.join(__dirname, PY_DIST_FOLDER)
  return require('fs').existsSync(fullPath)
}

const getScriptPath = () => {
  if (!guessPackaged()) {
    return path.join(__dirname, PY_FOLDER, PY_MODULE + '.py')
  }
  if (process.platform === 'win32') {
    return path.join(__dirname, PY_DIST_FOLDER, PY_MODULE, PY_MODULE + '.exe')
  }
  return path.join(__dirname, PY_DIST_FOLDER, PY_MODULE, PY_MODULE)
}

const createPyProc = () => {
  const port = '4242'
  const script = getScriptPath()

  // const script = path.join(__dirname,'src', 'server.py')
  // pyProc = require('child_process').spawn('python', [script, port])
  if(guessPackaged()){
    pyProc = require('child_process').execFile(script, [port])
  } else {
    console.log('spawn: '+script)
    pyProc = require('child_process').spawn('python', [script, port])
  }
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

  console.log(`initialize main.js`)
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