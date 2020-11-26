/**
 * Sheller.js用来解析shell命令
 */

const ErrInfo = function(config = {}) {
    // @stateCode
    // 0: input Error
    // 1: need return helpInfo
    this.stateCode = config.stateCode || 0
    this.errInfo = config.errInfo || ''
}

class Sheller{
    constructor(){
        this.options = {}
        this.commands = []
        this.n = ''
        this.v = ''
        this.cmdHeader = ''
        this.u = ''
    }
}

Sheller.prototype['name'] = function(n) {
    this.n = n
    return this
}

Sheller.prototype['version'] = function(v) {
    this.v = v
    return this
}

Sheller.prototype['setCmdHeader'] = function(header) {
    this.cmdHeader = header
    return this
}

/**
 * option item: 
 * {
 *  op_name : {
 *      call: false,
 *      op: op_name,
 *      info: '',
 *      hook_func: null
 *  }
 * }
 */
Sheller.prototype['option'] = function(op, info='', hook_func=null) {
    if(!op){
        const errInfo = new ErrInfo({
            stateCode: 0,
            errInfo: 'No exist option'
        })
        this.quit(errInfo)
    }
    if(this.options[op]){
        const errInfo = new ErrInfo({
            stateCode: 0,
            errInfo: 'repeat option!'
        })
        this.quit(errInfo)
    }
    const option = {
        'old_key': {
            call: false
        }
    }
    option['old_key'].op = op
    option['old_key'].info = info
    option['old_key'].hook_func = hook_func

    Object.defineProperty(option, op, 
        Object.getOwnPropertyDescriptor(option, 'old_key'))
    delete option['old_key']

    Object.assign(this.options, option)
    return this
}

Sheller.prototype['parse'] = function(command, options) {
    const _self = this
    if(options && options.from == 'user'){
        const args = command.trim().split(' ')
        args.forEach((item, index) => {

            if( item == '' )  return

            // 验证 cmdHeader
            if( index == 0 ){
                if(_self.cmdHeader != '' && item != _self.cmdHeader){
                    const errInfo = new ErrInfo({
                        stateCode: 0,
                        errInfo: 'comHeader err!'
                    })
                    this.quit(errInfo)
                } else {
                    return
                } 
            }
            
            // 若该options被注册
            if( _self.options[item] ){
                // hook_func only exec once times!
                if(!_self.options[item].call && _self.options[item].hook_func){
                    _self.options[item].hook_func.apply()
                }
                _self.options[item].call = true
                return
            }

            // 无法解析的指令
            this.quit(new ErrInfo({
                stateCode: 0,
                errInfo: 'can not parse option '+item
            }))
        })
    }else{
        // such: node app.js -h
        // TODO
    }
}

Sheller.prototype['usage'] = function(usage){
    this.u = usage
    return this
}

/**
 * print format help info
 * when input err occur, call this.helpInformation() and return msg
 */
Sheller.prototype['helpInformation'] = function(){
    let template_help = '\n'
    if(this.u){
        template_help += 'Usage: '+this.cmdHeader+' '+this.u+'\n\n'
    }
    if(this.options){
        template_help += 'Options: \n'
        for(let i in this.options){
            template_help += this.options[i].op+',    '+this.options[i].info+'\n'
        }
    }
    return template_help
}

// TODO
Sheller.prototype['command'] = function(cmd) {
    if(!cmd){
        const errInfo = new ErrInfo({
            stateCode: 0,
            errInfo: 'No exist command'
        })
        this.quit(errInfo)
    }
    const command = {
        call: false
    }
    
    return this
}


Sheller.prototype['quit'] = function(errInfo) {
    console.log(this.helpInformation())
    throw errInfo.errInfo
}

module.exports = {
    Sheller
}