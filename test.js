// const { program } = require('commander')
// const package = require('../QSim/views/package.json')
// const { exec, spawn } = require('child_process')

const { Command } = require('commander'); // include commander in git clone of commander repo
const program = new Command();

try{

    program.exitOverride()
    program
    .version('0.0.1')
    .option('-C, --chdir <path>', 'change the working directory')
    .option('-c, --config <path>', 'set config path. defaults to ./deploy.conf')
    .option('-T, --no-tests', 'ignore test hook');
  
  program
    .command('setup [env]')
    .description('run setup commands for all envs')
    .option('-s, --setup_mode [mode]', 'Which setup mode to use')
    .action(function(env, options) {
      const mode = options.setup_mode || 'normal';
      env = env || 'all';
      console.log('setup for %s env(s) with %s mode', env, mode);
    });
  
  program
    .command('exec <cmd>')
    .alias('ex')
    .description('execute the given remote cmd')
    .option('-e, --exec_mode <mode>', 'Which exec mode to use')
    .action(function(cmd, options) {
      console.log('exec "%s" using %s mode', cmd, options.exec_mode);
    }).on('--help', function() {
      console.log('  Examples:');
      console.log();
      console.log('    $ deploy exec sequential');
      console.log('    $ deploy exec async');
      console.log();
    });
  
    const argv = ['exec', '-h']
    program.parseAsync(argv, { from: 'user' })
}catch(e){
    console.log('Catch',e.name)
}
/*
program
    .name('qsim')
    .version(package.version, '-v', '-V', '--version')
    .usage('<command> [options]')
    .command('qsim <action>')
    .option('-d, --debug', 'debug source code')  
    .option('-q, --quit', 'quit program')  
    .option('-s, --save', 'save code from textarea')
    .option('-l, --lexer', 'generate lexer token')
    .option('-p, --parser', 'generate AST(Abstract syntax tree)')
    .option('-tpy, --transpy', 'translate QLight to python')
    .action(async (action, cmdObj) => {
        console.log('command run')
        console.log('action', action)
        if(cmdObj.debug){
            console.log('command debug!')
        }
        if(cmdObj.quit){
            console.log('command quit!')
        }
        if(cmdObj.save){
            console.log('command save!')
        }
        if(cmdObj.lexer){
            console.log('command lexer!')
        }
        if(cmdObj.parser){
            console.log('command parser!')
        }
        if(cmdObj.transpy){
            console.log('command transpy')
        }
        if(cmdObj.help){
            console.log('command help')
        }
    })

// program
//     .command('run')
//     .description('exec source code in textarea')
//     .option('-l, --lexer', 'generate lexer token')
//     .action(async () => {
//         console.log('command run')
//         if(program.lexer){
//             console.log('command lexer!')
//         }
//     })

// program
//     .command('--help')
//     .action(() => {
//         console.log('command --help')
//     })

// console.log('_helpLongFlag', program.helpInformation())

// program.on('--help', function(){  
//     console.log('');  
//     console.log('Examples:');  
//     console.log('  $ qsim --help');
//     console.log('  $ qsim run');
//    })

// program.parseAsync(['-l', 'run'], {from: 'user'})
program.parseAsync(['qsim','run', '-s', '-h'], {from: 'user'})
// program.parseAsync(['qsim','-s', 'run', '-l', '-d'], {from: 'user'})

if(program.quit){
    console.log('quit!')
}
if(program.save){
    console.log('save!')
}
if(program.lexer){
    console.log('lexer!')
}
if(program.parser){
    console.log('parser!')
}
if(program.transpy){
    console.log('transpy')
}
*/
// console.log('执行到这里了')
// const shell = '--help'

// exec(shell, {timeout: 5000}, (err, stdout, stderr) => {
//     console.log('err', err, err.signal)
//     console.log('stdout', stdout)
//     console.log('stderr', stderr)
// })

// const ls = spawn("node", ["-v"]);
// const ls = spawn("node");

// ls.stdout.on("data", data => {
//     console.log(`stdout: ${data}`);
// });

// ls.stderr.on("data", data => {
//     console.log(`stderr: ${data}`);
// });

// ls.on('error', (error) => {
//     console.log(`error: ${error.message}`);
// });

// ls.on("close", code => {
//     console.log(`child process exited with code ${code}`);
// });