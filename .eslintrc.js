module.exports = {
    root: true,
    parserOptions: {
      sourceType: 'module',
      ecmaVersion: 2015
    },
    env: {
      browser: true,
      node: true
    },
    extends: 'eslint:recommended',
    globals: {
      window: true,
      QSim: true
    },
    'rules': {
      // allow paren-less arrow functions
      'arrow-parens': 0,
      // allow async-await
      'generator-star-spacing': 0,
      'comma-dangle': 0,
      'no-trailing-spaces': 0,
      'space-before-function-paren': 0,
      'no-inner-declarations': 0,
      'indent': ['off', 2],
      'space-in-parens': 2,
      'func-call-spacing': 2,
      // allow debugger during development
      'no-debugger': process.env.NODE_ENV === 'production' ? 2 : 0
    }
  }