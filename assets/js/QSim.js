const QSim = {
  init: function (bandwidth, timewidth) {
    return new QSim.Circuit(bandwidth, timewidth)
  },
  Editor: {},
  Circuit: {},
  Gate: {}
}

Object.assign(QSim, {
  log: function () {
    console.log(...arguments)
    return '(log)'
  },

  warn: function () {
    console.warn(...arguments)
    return '(warn)'
  },

  error: function () {
    console.error(...arguments)
    return '(error)'
  },

  isUsefulNumber: function (n) {
    return isNaN(n) === false &&
      (typeof n === 'number' || n instanceof Number) &&
      n !== Infinity &&
      n !== -Infinity
  },

  isUsefulInteger: function (n) {
    return QSim.isUsefulNumber(n) && Number.isInteger(n)
  },

  // if arr1 includes arr2, return true
  // if arr1 == arr2, return false
  // arr2 is a proper subset of arr1
  includes: function (arr1, arr2) {
    return arr2.every(val => arr1.includes(val)) && arr1.length != arr2.length
  },

  printInTerminal: function () {

  }

})