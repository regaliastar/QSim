const QSim = {
    init: function(bandwidth, timewidth){
        return new QSim.Circuit(bandwidth, timewidth)
    },
    Editor: {},
    Circuit: {},
    Gate: {}
}

Object.assign(QSim, {

    warn: function(){
		console.warn( ...arguments )
		return '(warn)'
    },
    
	error: function(){
		console.error( ...arguments )
		return '(error)'
    },

    isUsefulNumber: function( n ){
		return isNaN( n ) === false && 
			( typeof n === 'number' || n instanceof Number ) &&
			n !==  Infinity &&
			n !== -Infinity
    },
    
	isUsefulInteger: function( n ){
		return QSim.isUsefulNumber( n ) && Number.isInteger( n )
    },

    printInTerminal: function(){
        
    }
    
})