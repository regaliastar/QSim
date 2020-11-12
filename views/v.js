const QSim = {
    init: function(bandwidth, timewidth){
        return new QSim.Circuit(bandwidth, timewidth)
    },
    Editor: {},
    Circuit: {},
    gate: {}
}


QSim.Editor = function( circuit, targetEl ){
    this.name = 'playground'
    const createDiv = function(){
		return document.createElement( 'div' )
    }
    const circuitEl = targetEl instanceof HTMLElement ? targetEl : createDiv()
    circuitEl.classList.add( 'Q-circuit' )
    if( typeof circuitEl.getAttribute( 'id' ) === 'string' ){

		this.domId = circuitEl.getAttribute( 'id' )
	}else {

		let domIdBase = this.name
			.replace( /^[^a-z]+|[^\w:.-]+/gi, '-' ),
		domId = domIdBase,
		domIdAttempt = 1

		while( document.getElementById( domId ) !== null ){

			domIdAttempt ++
			domId = domIdBase +'-'+ domIdAttempt
		}
		this.domId = domId
		circuitEl.setAttribute( 'id', this.domId )
    }
    circuitEl.circuit = circuit
    this.domElement = circuitEl

    const toolbarEl = createDiv()
	circuitEl.appendChild( toolbarEl )
    toolbarEl.classList.add( 'Q-circuit-toolbar' )
    
    const lockToggle = createDiv()
	toolbarEl.appendChild( lockToggle )
	lockToggle.classList.add( 'Q-circuit-button', 'Q-circuit-toggle', 'Q-circuit-toggle-lock' )
	lockToggle.setAttribute( 'title', 'Lock / unlock' )
    lockToggle.innerText = '🔓'
    
    const undoButton = createDiv()
	toolbarEl.appendChild( undoButton )
	undoButton.classList.add( 'Q-circuit-button', 'Q-circuit-button-undo' )
	undoButton.setAttribute( 'title', 'Undo' )
	undoButton.setAttribute( 'Q-disabled', 'Q-disabled' )
	undoButton.innerHTML = '⟲'
	window.addEventListener( 'Q.History undo is depleted', function( event ){

		if( event.detail.instance === circuit )
			undoButton.setAttribute( 'Q-disabled', 'Q-disabled' )
	})
	window.addEventListener( 'Q.History undo is capable', function( event ){

		if( event.detail.instance === circuit )
			undoButton.removeAttribute( 'Q-disabled' )
    })
    
    const redoButton = createDiv()
	toolbarEl.appendChild( redoButton )
	redoButton.classList.add( 'Q-circuit-button', 'Q-circuit-button-redo' )
	redoButton.setAttribute( 'title', 'Redo' )
	redoButton.setAttribute( 'Q-disabled', 'Q-disabled' )
	redoButton.innerHTML = '⟳'
	window.addEventListener( 'Q.History redo is depleted', function( event ){

		if( event.detail.instance === circuit )
			redoButton.setAttribute( 'Q-disabled', 'Q-disabled' )
	})
	window.addEventListener( 'Q.History redo is capable', function( event ){

		if( event.detail.instance === circuit )
			redoButton.removeAttribute( 'Q-disabled' )
	})

    const controlButton = createDiv()
	toolbarEl.appendChild( controlButton )
	controlButton.classList.add( 'Q-circuit-button', 'Q-circuit-toggle', 'Q-circuit-toggle-control' )
	controlButton.setAttribute( 'title', 'Create controlled operation' )
	controlButton.setAttribute( 'Q-disabled', 'Q-disabled' )
	controlButton.innerText = 'C'

    const swapButton = createDiv()
	toolbarEl.appendChild( swapButton )
	swapButton.classList.add( 'Q-circuit-button', 'Q-circuit-toggle-swap' )
	swapButton.setAttribute( 'title', 'Create swap operation' )
	swapButton.setAttribute( 'Q-disabled', 'Q-disabled' )
	swapButton.innerText = 'S'


	//  Create a circuit board container
	//  so we can house a scrollable circuit board.

	const boardContainerEl = createDiv()
	circuitEl.appendChild( boardContainerEl )
	boardContainerEl.classList.add( 'Q-circuit-board-container' )
	//boardContainerEl.addEventListener( 'touchstart', QSim.Editor.onPointerPress )
	boardContainerEl.addEventListener( 'mouseleave', function(){

		QSim.Editor.unhighlightAll( circuitEl )
	})

	const boardEl = createDiv()
	boardContainerEl.appendChild( boardEl )
	boardEl.classList.add( 'Q-circuit-board' )

	const backgroundEl = createDiv()
	boardEl.appendChild( backgroundEl )
	backgroundEl.classList.add( 'Q-circuit-board-background' )

    //  Create background highlight bars 
	//  for each row.

	for( let i = 0; i < circuit.bandwidth; i ++ ){

		const rowEl = createDiv()
		backgroundEl.appendChild( rowEl )
		rowEl.style.position = 'relative'
		rowEl.style.gridRowStart = i + 2
		rowEl.style.gridColumnStart = 1
		rowEl.style.gridColumnEnd = QSim.Editor.momentIndexToGridColumn( circuit.timewidth ) + 1
		rowEl.setAttribute( 'register-index', i + 1 )

		const wireEl = createDiv()
		rowEl.appendChild( wireEl )
		wireEl.classList.add( 'Q-circuit-register-wire' )
	}

//  Create background highlight bars 
	//  for each column.

	for( let i = 0; i < circuit.timewidth; i ++ ){

		const columnEl = createDiv()
		backgroundEl.appendChild( columnEl )
		columnEl.style.gridRowStart = 2
		columnEl.style.gridRowEnd = QSim.Editor.registerIndexToGridRow( circuit.bandwidth ) + 1
		columnEl.style.gridColumnStart = i + 3
		columnEl.setAttribute( 'moment-index', i + 1 )
	}


	//  Create the circuit board foreground
	//  for all interactive elements.

	const foregroundEl = createDiv()
	boardEl.appendChild( foregroundEl )
	foregroundEl.classList.add( 'Q-circuit-board-foreground' )

    //  Add “Select All” toggle button to upper-left corner.

	const selectallEl = createDiv()
	foregroundEl.appendChild( selectallEl )
	selectallEl.classList.add( 'Q-circuit-header', 'Q-circuit-selectall' )	
	selectallEl.setAttribute( 'title', 'Select all' )
	selectallEl.setAttribute( 'moment-index', '0' )
	selectallEl.setAttribute( 'register-index', '0' )
	selectallEl.innerHTML = '&searr;'


    //  Add register index symbols to left-hand column.
	
	for( let i = 0; i < circuit.bandwidth; i ++ ){

		const 
		registerIndex = i + 1,
		registersymbolEl = createDiv()
		
		foregroundEl.appendChild( registersymbolEl )
		registersymbolEl.classList.add( 'Q-circuit-header', 'Q-circuit-register-label' )
		registersymbolEl.setAttribute( 'title', 'Register '+ registerIndex +' of '+ circuit.bandwidth )
		registersymbolEl.setAttribute( 'register-index', registerIndex )
		registersymbolEl.style.gridRowStart = QSim.Editor.registerIndexToGridRow( registerIndex )
		registersymbolEl.innerText = registerIndex
	}

    
	//  Add “Add register” button.
	
	const addRegisterEl = createDiv()
	foregroundEl.appendChild( addRegisterEl )
	addRegisterEl.classList.add( 'Q-circuit-header', 'Q-circuit-register-add' )
	addRegisterEl.setAttribute( 'title', 'Add register' )
	addRegisterEl.style.gridRowStart = QSim.Editor.registerIndexToGridRow( circuit.bandwidth + 1 )
	addRegisterEl.innerText = '+'


	//  Add moment index symbols to top row.

	for( let i = 0; i < circuit.timewidth; i ++ ){

		const 
		momentIndex = i + 1,
		momentsymbolEl = createDiv()

		foregroundEl.appendChild( momentsymbolEl )
		momentsymbolEl.classList.add( 'Q-circuit-header', 'Q-circuit-moment-label' )
		momentsymbolEl.setAttribute( 'title', 'Moment '+ momentIndex +' of '+ circuit.timewidth )
		momentsymbolEl.setAttribute( 'moment-index', momentIndex )
		momentsymbolEl.style.gridColumnStart = QSim.Editor.momentIndexToGridColumn( momentIndex )
		momentsymbolEl.innerText = momentIndex
	}


	//  Add “Add moment” button.
	
	const addMomentEl = createDiv()
	foregroundEl.appendChild( addMomentEl )
	addMomentEl.classList.add( 'Q-circuit-header', 'Q-circuit-moment-add' )
	addMomentEl.setAttribute( 'title', 'Add moment' )
	addMomentEl.style.gridColumnStart = QSim.Editor.momentIndexToGridColumn( circuit.timewidth + 1 )
	addMomentEl.innerText = '+'

    //  Add input values.

	circuit.qubits.forEach( function( qubit, i ){

		const 
		rowIndex = i + 1,
		inputEl = createDiv()
		
		inputEl.classList.add( 'Q-circuit-header', 'Q-circuit-input' )
		inputEl.setAttribute( 'title', `Qubit #${ rowIndex } starting value` )
		inputEl.setAttribute( 'register-index', rowIndex )
		inputEl.style.gridRowStart = QSim.Editor.registerIndexToGridRow( rowIndex )
        // inputEl.innerText = qubit.beta.toText()
        inputEl.innerText = 'q'+i
		foregroundEl.appendChild( inputEl )
	})
}

Object.assign( QSim.Editor, {
	index: 0,
	dragEl: null,
	gridColumnToMomentIndex: function( gridColumn  ){ return +gridColumn - 2 },
	momentIndexToGridColumn: function( momentIndex ){ return momentIndex + 2 },
	gridRowToRegisterIndex:  function( gridRow ){ return +gridRow - 1 },
	registerIndexToGridRow:  function( registerIndex ){ return registerIndex + 1 },
	gridSize: 4,//  CSS: grid-auto-columns = grid-auto-rows = 4rem.
	pointToGrid: function( p ){
		const rem = parseFloat( getComputedStyle( document.documentElement ).fontSize )
		return 1 + Math.floor( p / ( rem * QSim.Editor.gridSize ))
	},
	gridToPoint: function( g ){
		const  rem = parseFloat( getComputedStyle( document.documentElement ).fontSize )
		return rem * QSim.Editor.gridSize * ( g - 1 )
	},
	getInteractionCoordinates: function( event, pageOrClient ){

		if( typeof pageOrClient !== 'string' ) pageOrClient = 'client'//page
		if( event.changedTouches && 
			event.changedTouches.length ) return {

			x: event.changedTouches[ 0 ][ pageOrClient +'X' ],
			y: event.changedTouches[ 0 ][ pageOrClient +'Y' ]
		}
		return {

			x: event[ pageOrClient +'X' ],
			y: event[ pageOrClient +'Y' ]
		}
	},
	createPalette: function( targetEl ){

		if( typeof targetEl === 'string' ) targetEl = document.getElementById( targetEl )	

		const 
		paletteEl = targetEl instanceof HTMLElement ? targetEl : document.createElement( 'div' ),
		randomRangeAndSign = function(  min, max ){

			const r = min + Math.random() * ( max - min )
			return Math.floor( Math.random() * 2 ) ? r : -r
		}

		paletteEl.classList.add( 'Q-circuit-palette' )

		'HXYZPT*'
		.split( '' )
		.forEach( function( symbol ){

            const gate = QSim.gate.findBySymbol( symbol )
            // console.log(gate)

			const operationEl = document.createElement( 'div' )
			paletteEl.appendChild( operationEl )
			operationEl.classList.add( 'Q-circuit-operation' )
			operationEl.classList.add( 'Q-circuit-operation-'+ gate.nameCss )
			operationEl.setAttribute( 'gate-symbol', symbol )
			operationEl.setAttribute( 'title', gate.name )

			const tileEl = document.createElement( 'div' )
			operationEl.appendChild( tileEl )
			tileEl.classList.add( 'Q-circuit-operation-tile' )
			if( symbol !== '*' ) tileEl.innerText = symbol

			;[ 'before', 'after' ].forEach( function( layer ){

				tileEl.style.setProperty( '--Q-'+ layer +'-rotation', randomRangeAndSign( 0.5, 4 ) +'deg' )
				tileEl.style.setProperty( '--Q-'+ layer +'-x', randomRangeAndSign( 1, 4 ) +'px' )
				tileEl.style.setProperty( '--Q-'+ layer +'-y', randomRangeAndSign( 1, 3 ) +'px' )
			})
		})

		paletteEl.addEventListener( 'mousedown',  QSim.Editor.onPointerPress )
		paletteEl.addEventListener( 'touchstart', QSim.Editor.onPointerPress )
		return paletteEl
	}
})

QSim.Circuit = function( bandwidth, timewidth ){



	//  How many qubits (registers) shall we use?

	if( !bandwidth) bandwidth = 3
	this.bandwidth = bandwidth


	//  How many operations can we perform on each qubit?
	//  Each operation counts as one moment; one clock tick.

	if( !timewidth) timewidth = 5
	this.timewidth = timewidth


	//  We’ll start with Horizontal qubits (zeros) as inputs
	//  but we can of course modify this after initialization.

	this.qubits = new Array( bandwidth ).fill( 'test' )


	//  What operations will we perform on our qubits?
	
	this.operations = []


	//  Does our circuit need evaluation?
	//  Certainly, yes!
	// (And will again each time it is modified.)

	this.needsEvaluation = true
	

	//  When our circuit is evaluated 
	//  we store those results in this array.

	this.results = []
	this.matrix  = null

    this.toDom = ( targetEl ) => {
        return new QSim.Editor( this, targetEl ).domElement
    }
}

const QSim_gate = {
    'H':'',
    'X':'',
    'Y':'',
    'Z':'',
    'P':'',
    'T':'',
    '*':''
}

QSim.Editor.unhighlightAll = function( circuitEl ){

	Array.from( circuitEl.querySelectorAll( 

		'.Q-circuit-board-background > div,'+
		'.Q-circuit-board-foreground > div'
	))
	.forEach( function( el ){

		el.classList.remove( 'Q-circuit-cell-highlighted' )
	})
}

QSim.gate.findBySymbol = symbol => {
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