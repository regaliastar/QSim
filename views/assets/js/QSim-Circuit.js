QSim.Circuit = function (bandwidth, timewidth) {
    if (!bandwidth) bandwidth = 3
    this.bandwidth = bandwidth
    this.set_bandwidth = bandwidth => {
        this.bandwidth = bandwidth
        this.qubits = new Array(bandwidth).fill('test')
    }

    if (!timewidth) timewidth = 5
    this.timewidth = timewidth
    this.set_timewidth = timewidth => { this.timewidth = timewidth }

    this.qubits = new Array(bandwidth).fill('test')

    this.operations = []

    this.needsEvaluation = true

    this.results = []
    this.matrix = null

    this.toDom = (targetEl) => {
        return new QSim.Editor(this, targetEl).domElement
    }

    // 绘制的是gates信息
    // gates的 item = {
    //     gate: null,
    //     registerIndices: [],
    //     isControlled: false,
    //     momentIndex: 1
    // }
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
        scan = QSim.Circuit.Scanner(txt)
        this.gates = scan.gates
        this.qubits_count = scan.qubits_count
        this.maxMomentIndex = scan.maxMomentIndex
    }
}


//////////////////////////////////
//                              //
//   文本分析，将代码转为量子门   //
//                              //
//////////////////////////////////


QSim.Circuit.Scanner = (txt) => {

    function getNextChar() {
        ptr++
        if (ptr >= cont.length) {
            return '\0'
        }
        return cont[ptr]
    }
    function recognizeId(ch) {
        let state = 0
        let str = ''
        while (state != 2) {
            if (state == 0) {
                if (/^[A-Za-z]+$/.test(ch) || ch == '_') {
                    state = 1
                    str += ch
                }
            }
            if (state == 1) {
                ch = getNextChar()
                if (/^[A-Za-z]+$/.test(ch) || ch == '_') {
                    state = 1
                    str += ch
                } else {
                    state = 2
                }
            }
        }
        ptr--
        return str
    }

    function recognizeInteger(ch) {
        let state = 0
        let str = ''
        while (state != 2) {
            if (state == 0) {
                if (/^\d+$/.test(ch)) {
                    state = 1
                    str += ch
                }
            }
            if (state == 1) {
                ch = getNextChar()
                if (/^\d+$/.test(ch)) {
                    state = 1
                    str += ch
                } else {
                    state = 2
                }
            }
        }
        ptr--
        return str
    }

    const cont = txt.trim()
    // console.log('Scanner source code: ',cont)

    let ptr = 0
    let state = 0   //state是必要的，为了能够将门和其他的语句区分开
    let qubit_state = 0
    let result = {
        gates: [],
        qubits_count: 0,
        maxMomentIndex: 0,
    }
    let item = {
        gate: null,
        registerIndices: [],
        isControlled: false,
        momentIndex: 1
    }
    let momentIndex = 1
    while (ptr < cont.length) {
        if (state == 0 && (/^[A-Za-z]+$/.test(cont.charAt(ptr)) || cont.charAt(ptr) == '_')) {
            iden = recognizeId(cont.charAt(ptr))
            if (QSim.Gate.totalGate.indexOf(iden) != -1) {
                state = 1
                // console.log(1, iden)
                item.gate = QSim.Gate.findBySymbol(iden)
            }
            else if (iden == 'quantum') {
                qubit_state = 1
            }
        }
        else if ((qubit_state == 1 || state == 1) && /^\d+$/.test(cont.charAt(ptr))) {
            // console.log(2, cont.charAt(ptr))
            let s_int = recognizeInteger(cont.charAt(ptr))
            // console.log('s_int', s_int)
            s_int = Number.parseInt(s_int)
            if (state == 1) {
                item.registerIndices.push(++s_int)
                if (item.registerIndices.length > 1) item.isControlled = true
            }
            if (qubit_state == 1) {
                result.qubits_count = s_int
                qubit_state = 0
            }
        }
        else if (state == 1 && cont.charAt(ptr) == '\n') {
            state = 0
            // console.log(3, cont.charAt(ptr))
            item.momentIndex = momentIndex
            result.gates.push(JSON.parse(JSON.stringify(item)))
            item = {
                gate: null,
                registerIndices: [],
                isControlled: false,
                momentIndex: 1
            }
            momentIndex++
        }
        ptr++
    }
    if (state == 1) {
        state = 0
        item.momentIndex = momentIndex
        result.gates.push(JSON.parse(JSON.stringify(item)))
    }

    // 将result的momentIndex尽可能压缩
    let momentIndexCont = new Array(result.qubits_count).fill(1)
    let maxMomentIndex = 0
    for (let i = 0; i < result.gates.length; i++) {
        if (result.gates[i].registerIndices.length == 1) {
            let index = result.gates[i].registerIndices[0] - 1
            result.gates[i].momentIndex = momentIndexCont[index]
            maxMomentIndex < momentIndexCont[index] ? maxMomentIndex = momentIndexCont[index] : momentIndexCont[index]
            momentIndexCont[index]++
        } else {
            const index_0 = result.gates[i].registerIndices[0] - 1,
                index_1 = result.gates[i].registerIndices[1] - 1,
                max = Math.max(momentIndexCont[index_0], momentIndexCont[index_1])

            result.gates[i].momentIndex = max
            maxMomentIndex < max ? maxMomentIndex = max : max

            momentIndexCont[index_0] = max + 1
            momentIndexCont[index_1] = max + 1
        }
    }
    result.maxMomentIndex = maxMomentIndex

    return result
}


//////////////////////////////////
//                              //
//   语义，检测scan是否正确      //
//                              //
//////////////////////////////////


QSim.Circuit.checkScan = (scan) => {

    // 先检查 qubits_count
    const qubits_count = scan.qubits_count
    if (!QSim.isUsefulInteger(qubits_count) || qubits_count == 0) return false

    // 检查 Gates
    const gates = scan.gates
    for (let i = 0; i < gates.length; i++) {
        if (gates[i].registerIndices.length == 0) return false

    }

    return true

}

Object.assign(QSim.Circuit.prototype, {
    set$: function (gate, momentIndex, registerIndices) {

        const circuit = this

        //  Is this a valid gate?

        if (typeof gate === 'string') gate = QSim.Gate.findBySymbol(gate)

        if (QSim.isUsefulNumber(momentIndex) !== true ||
            Number.isInteger(momentIndex) !== true ||
            momentIndex < 1 || momentIndex > this.timewidth) {

            return Q.error(`Q.Circuit attempted to add a gate to circuit #${this.index} at a moment index that is not valid:`, momentIndex)
        }

        //  Are these valid register indices?

        if (typeof registerIndices === 'number') registerIndices = [registerIndices]
        if (registerIndices instanceof Array !== true) return QSim.error(`Q.Circuit attempted to add a gate to circuit #${this.index} at moment #${momentIndex} with an invalid register indices array:`, registerIndices)
        if (registerIndices.length === 0) return QSim.error(`Q.Circuit attempted to add a gate to circuit #${this.index} at moment #${momentIndex} with an empty register indices array:`, registerIndices)
        if (registerIndices.reduce(function (accumulator, registerIndex) {

            return (
                accumulator &&
                registerIndex > 0 &&
                registerIndex <= circuit.bandwidth
            )

        }, false)) {

            return QSim.warn(`QSim.Circuit attempted to add a gate to circuit #${this.index} at moment #${momentIndex} with some out of range qubit indices:`, registerIndices)
        }

        // console.log('registerIndices', registerIndices)
        //  Ok, now we can check if this set$ command
        //  is redundant.

        const
            isRedundant = !!circuit.operations.find(function (operation) {

                return (

                    momentIndex === operation.momentIndex &&
                    gate === operation.gate &&
                    registerIndices.length === operation.registerIndices.length &&
                    registerIndices.every(val => operation.registerIndices.includes(val))
                )
            })


        //  If it’s NOT redundant 
        //  then we’re clear to proceed.

        if (isRedundant !== true) {


            //  If there’s already an operation here,
            //  we’d better get rid of it!
            //  This will also entirely remove any multi-register operations
            //  that happen to have a component at this moment / register.

            this.clear$(momentIndex, registerIndices)


            //  Finally. 
            //  Finally we can actually set this operation.
            //  Aren’t you glad we handle all this for you?
            swap_gate = QSim.Gate.findBySymbol('S')
            const
                isControlled = registerIndices.length > 1 && gate !== swap_gate,
                operation = {

                    gate,
                    momentIndex,
                    registerIndices,
                    isControlled
                }
            this.gates.push(operation)


            //  IMPORTANT!
            //  Operations must be sorted properly
            //  for toTable to work reliably with
            //  multi-register operations!!

            this.sort$()

            // update code in html by drag circuitEl

            QSim.Editor.updateCode(circuit)

            // const source_code = document.getElementById('playground-input').value.trim()
            // scan = QSim.Circuit.Scanner(source_code)
            // QSim.log('clear', source_code)
            // if( QSim.Circuit.checkScan(scan) ){
            //     updatePlayground()
            // }

            //  Emit an event that we have set an operation
            //  on this circuit.


            window.dispatchEvent(new CustomEvent(

                'QSim.Circuit.set$', {
                    detail: {

                        circuit,
                        operation
                    }
            }
            ))

        }
        return circuit
    },


    clear$: function (momentIndex, registerIndices) {

        const circuit = this

        //  Validate our arguments.

        if (arguments.length !== 2)
            QSim.warn(`Q.Circuit.clear$ expected 2 arguments but received ${arguments.length}.`)
        if (QSim.isUsefulInteger(momentIndex) !== true)
            return QSim.error(`Q.Circuit attempted to clear an input on Circuit #${circuit.index} using an invalid moment index:`, momentIndex)
        if (QSim.isUsefulInteger(registerIndices)) registerIndices = [registerIndices]
        if (registerIndices instanceof Array !== true)
            return QSim.error(`Q.Circuit attempted to clear an input on Circuit #${circuit.index} using an invalid register indices array:`, registerIndices)


        //  Let’s find any operations 
        //  with a footprint at this moment index and one of these register indices
        //  and collect not only their content, but their index in the operations array.
        // (We’ll need that index to splice the operations array later.)

        const foundOperations = circuit.gates.reduce(function (filtered, operation, o) {

            if (operation.momentIndex === momentIndex &&
                operation.registerIndices.some(function (registerIndex) {

                    return registerIndices.includes(registerIndex)
                })
            ) filtered.push({

                index: o,
                momentIndex: operation.momentIndex,
                registerIndices: operation.registerIndices,
                gate: operation.gate
            })
            return filtered

        }, [])


        //  Because we held on to each found operation’s index
        //  within the circuit’s operations array
        //  we can now easily splice them out of the array.

        foundOperations.reduce(function (deletionsSoFar, operation) {

            circuit.gates.splice(operation.index - deletionsSoFar, 1)
            return deletionsSoFar + 1

        }, 0)


        //  IMPORTANT!
        //  Operations must be sorted properly
        //  for toTable to work reliably with
        //  multi-register operations!!

        this.sort$()

        // update code in html by drag circuitEl
        QSim.Editor.updateCode(circuit)
        // const source_code = document.getElementById('playground-input').value.trim()
        // scan = QSim.Circuit.Scanner(source_code)
        // QSim.log('clear', source_code)
        // if( QSim.Circuit.checkScan(scan) ){
        //     updatePlayground()
        // }


        // QSim.log(source)
        foundOperations.forEach(function (operation) {

            window.dispatchEvent(new CustomEvent(

                'QSim.Circuit.clear$', {
                    detail: {

                        circuit,
                        momentIndex,
                        registerIndices: operation.registerIndices
                    }
            }
            ))
        })

        //  Enable that “fluent interface” method chaining :)

        return circuit
    },


    sort$: function () {


        //  Sort this circuit’s operations
        //  primarily by momentIndex,
        //  then by the first registerIndex.

        this.gates.sort(function (a, b) {

            if (a.momentIndex === b.momentIndex) {


                //  Note that we are NOT sorting registerIndices here!
                //  We are merely asking which set of indices contain
                //  the lowest register index.
                //  If we instead sorted the registerIndices 
                //  we could confuse which qubit is the controller
                //  and which is the controlled!

                return Math.min(...a.registerIndices) - Math.min(b.registerIndices)
            }
            else {

                return a.momentIndex - b.momentIndex
            }
        })
        return this
    },

})