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
     * like 
     * `
     * H 0
     * x 0 1
     * `
     */
    this.addGates = (str) => {
        if(!str){
            str = 
            `H 0
            X 0 1`
		}
		arr = []
        for(let i = 0; i < str.length; i++){
            const reg_alpha = /^[A-Za-z]+$/
            if(str.charAt(i) == '\n'){
                
            }else if(str.charAt(i) == ' '){

            }else if(reg_alpha.test(str.charAt(i))){

            }else{
                // 是数字

            }
		}
		return arr
    }
}

