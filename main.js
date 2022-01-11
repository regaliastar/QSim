const { app, BrowserWindow, Menu, shell } = require('electron')
const path = require('path')
const glob = require('glob')
const YAML = require('yamljs')
const fs = require('fs')

/**
* 读取配置文件 _config.yml
*/
const { 
  _windowSize,
  _server,
  _env
} = YAML.parse(fs.readFileSync(path.join(__dirname, '_config.yml')).toString())

let pyProc = null

const createPyProc = () => {
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
    if (!guessPackaged() || _env === 'dev') {
      return path.join(__dirname, PY_FOLDER, PY_MODULE + '.py')
    }
    if (process.platform === 'win32') {
      return path.join(__dirname, PY_DIST_FOLDER, PY_MODULE + '.exe')
    }
    return path.join(__dirname, PY_DIST_FOLDER, PY_MODULE)
  }
  const script = getScriptPath()
  console.log('guessPackaged: '+guessPackaged()+'  script: '+script)

  // 判断 python服务器 是否被打包
  if (guessPackaged() && _env !== 'dev') {
    pyProc = require('child_process').execFile(script, [_server.port])
  } else {
    console.log('dev')
    pyProc = require('child_process').spawn('python', [script, _server.port])
  }

  if (pyProc != null) {
    console.log('child process success')
  }
}

// quit python process
const exitPyProc = () => {
  pyProc.kill()
  pyProc = null
}

function createWindow() {
  const win = new BrowserWindow({
    width: _windowSize.width,
    height: _windowSize.height,
    webPreferences: {
      nodeIntegration: true,
      enableRemoteModule: true
    }
  })

  win.loadFile('index.html')
  // 打开控制台
  win.webContents.openDevTools()
}

function initMenu() {
  const menuTemplate = [
    {
      label: 'File',
      submenu: [
        {
          label: 'Exit',
          role: 'quit'
        }
      ]
    },
    {
      label: 'Edit',
      submenu: [
        {
          label: 'Undo'
        },
        {
          label: 'Redo'
        },
        {
          type: 'separator'
        },
        {
          label: 'Cut',
          role: 'cut',
          accelerator: 'CmdOrCtrl+X'
        },
        {
          label: 'Copy',
          role: 'copy',
          accelerator: 'CmdOrCtrl+C'
        },
        {
          label: 'Paste',
          role: 'paste',
          accelerator: 'CmdOrCtrl+V'
        },
        {
          label: 'Delete',
          role: 'delete'
        },
        {
          type: 'separator'
        },
        {
          label: 'select All',
          role: 'selectAll'
        }
      ]
    },
    {
      label: 'View',
      submenu: [
        {
          label: 'Reload',
          role: 'reload'
        },
        {
          type: 'separator'
        },
        {
          label: 'Zoom in',
          role: 'zoomin'
        },
        {
          label: 'Zoom out',
          role: 'zoomout'
        },
        {
          label: 'Toggle Full Screen',
          role: 'togglefullscreen'
        }
      ]
    },
    {
      label: 'Window',
      submenu: [
        {
          label: 'Minimize',
          role: 'minimize'
        }
      ]
    },
    {
      label: 'Help',
      submenu: [
        {
          label: 'Document',
          click: function(){
            shell.openExternal('https://github.com/regaliastar/QSim')
          }
        }
      ]
    }
  ]

  const appMenu = Menu.buildFromTemplate(menuTemplate)
  Menu.setApplicationMenu(appMenu)
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

  app.on('ready', () => {
    createPyProc()
    initMenu()
  })
  app.on('will-quit', exitPyProc)
}

// Require each JS file in the main-process dir
function loadDemos() {
  const files = glob.sync(path.join(__dirname, 'main-process/*.js'))
  files.forEach((file) => { require(file) })
}

initialize()