QSim.Circuit = function( bandwidth, timewidth ){
	if( !bandwidth) bandwidth = 3
	this.bandwidth = bandwidth

	if( !timewidth) timewidth = 5
	this.timewidth = timewidth

	this.qubits = new Array( bandwidth ).fill( 'test' )

	this.operations = []

	this.needsEvaluation = true

	this.results = []
	this.matrix  = null

    this.toDom = ( targetEl ) => {
        return new QSim.Editor( this, targetEl ).domElement
    }

    this.gates = []

    /**
     * @param {string} str 
     * 根据文本信息生成量子门集合
     * like 
     * `
     * H 0
     * x 0 1
     * `
     */
    this.set_source_code = txt => {
        this.gates = QSim.Circuit.Scanner(txt)
    }
}

// 文本分析，将代码转为量子门
QSim.Circuit.Scanner = (txt) => {
    function recognizeId(ch){
        let state = 0
        let str = ''
        while(state != 2){
            if(state == 0){
                if(/^[A-Za-z]+$/.test(ch) || ch == '_'){
                    state = 1
                    str += ch
                }
            }
            if(state == 1){
                ch = cont[++ptr]
                if(/^[A-Za-z]+$/.test(ch) || ch == '_'){
                    state = 1
                    str += ch
                }else{
                    state = 2
                }
            }
        }
        ptr --
        return str
    }

    function recognizeInteger(ch){
        let state = 0
        let str = ''
        while(state != 2){
            if(state == 0){
                if(/^\d+$/.test(ch)){
                    state = 1
                    str += ch
                }
            }
            if(state == 1){
                ch = cont[++ptr]
                if(/^\d+$/.test(ch)){
                    state = 1
                    str += ch
                }else{
                    state = 2
                }
            }
        }
        ptr --
        return str
    }

    const cont = txt.trim()

    let ptr = 0
    let state = 0   //state是必要的，为了能够将门和其他的语句区分开
    let result = []
    let item = {
        gate: null,
        registerIndices: [],
        isControlled: false,
        momentIndex: 1
    }
    let momentIndex = 1
    while(ptr < cont.length){
        if(state == 0 && (/^[A-Za-z]+$/.test(cont.charAt(ptr)) || cont.charAt(ptr) == '_')){
            iden = recognizeId(cont.charAt(ptr))
            if(QSim.Gate.totalGate.indexOf(iden) != -1){
                state = 1
                // console.log(1, iden)
                item.gate = QSim.Gate.findBySymbol(iden)
            }
        }
        else if (state == 1 && /^\d+$/.test(cont.charAt(ptr))){
            // console.log(2, cont.charAt(ptr))
            let s_int = recognizeInteger(cont.charAt(ptr))
            // console.log('s_int', s_int)
            s_int = Number.parseInt(s_int)
            item.registerIndices.push(++s_int)
            if(item.registerIndices.length > 1) item.isControlled = true
        }
        else if(state == 1 && cont.charAt(ptr) == '\n'){
            state = 0
            // console.log(3, cont.charAt(ptr))
            item.momentIndex = momentIndex
            result.push(JSON.parse(JSON.stringify(item)))
            item = {
                gate: null,
                registerIndices: [],
                isControlled: false,
                momentIndex: 1
            }
            momentIndex ++
        }
        ptr ++
    }
    if(state == 1){
        state = 0
        item.momentIndex = momentIndex
        result.push(JSON.parse(JSON.stringify(item)))
    }
    return result
}