const QSim_Gate = {
    'H':'',
    'X':'',
    'Y':'',
    'Z':'',
    'P':'',
    'T':'',
    '*':''
}

QSim.Gate.findBySymbol = symbol => {
    const contain = {
        'H':{
            symbol:    'H',
            nameCss: 'hadamard',
            name:    'Hadamard'
        },
        'P':{
            symbol:    'P',
		    name:      'Phase',
		    nameCss:   'phase',
        },
        'X':{
            symbol:    'X',
            name:      'Pauli X',
            nameCss:   'pauli-x',
        },
        'Y':{
            symbol:    'Y',
            name:      'Pauli Y',
            nameCss:   'pauli-y',
        },
        'Z':{
            symbol:    'Z',
		    name:      'Pauli Z',
		    nameCss:   'pauli-z',
        },
        'T':{
            symbol:    'T',
		    name:      'π ÷ 8',
		    nameCss:   'pi8',
        },
        'I':{
            symbol:    'I',
            name:      'Identity',
            nameCss:   'identity',
        },
        'CURSOR':{
            symbol:    '*',
		    name:      'Identity',
		    nameCss:   'identity',
        }
    }
    return (
        Object
        .values( contain )
        .find( function( item ){

            if( typeof symbol === 'string' && 
                typeof item[ 'symbol' ] === 'string' ){

                return symbol.toLowerCase() === item[ 'symbol' ].toLowerCase()
            }
            return symbol === item[ 'symbol' ]
        })
    )
}