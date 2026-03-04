let board
let currentPlayer
let mode
let starter
let gameOver=false


function startGame(selectedMode, firstMove="player"){

mode = selectedMode
starter = firstMove
gameOver = false

board = [
[" "," "," "],
[" "," "," "],
[" "," "," "]
]

createBoard()

if(mode==="ai"){

if(starter==="ai"){

currentPlayer="X"

document.getElementById("status").innerText="AI starts"

setTimeout(aiMove,400)

}
else{

currentPlayer="O"

document.getElementById("status").innerText="Player Turn"

}

}
else{

currentPlayer="X"

document.getElementById("status").innerText="Player X Turn"

}

}


function createBoard(){

const boardDiv = document.getElementById("board")

boardDiv.innerHTML=""

for(let i=0;i<3;i++){
for(let j=0;j<3;j++){

let cell = document.createElement("div")

cell.className="cell"

cell.onclick = ()=> makeMove(i,j)

boardDiv.appendChild(cell)

}
}

renderBoard()

}


function renderBoard(){

let cells = document.querySelectorAll(".cell")

cells.forEach((cell,index)=>{

let r = Math.floor(index/3)
let c = index%3

cell.innerText = board[r][c]

})

}


function makeMove(i,j){

if(gameOver) return
if(board[i][j]!=" ") return


if(mode==="ai"){

if(currentPlayer!=="O") return

board[i][j]="O"

renderBoard()

if(checkWinner("O")){
document.getElementById("status").innerText="Player Wins!"
gameOver=true
return
}

if(isDraw()){
document.getElementById("status").innerText="Draw!"
gameOver=true
return
}

currentPlayer="X"

document.getElementById("status").innerText="AI thinking..."

setTimeout(aiMove,300)

}
else{

board[i][j]=currentPlayer

renderBoard()

if(checkWinner(currentPlayer)){
document.getElementById("status").innerText=currentPlayer+" Wins!"
gameOver=true
return
}

if(isDraw()){
document.getElementById("status").innerText="Draw!"
gameOver=true
return
}

currentPlayer = currentPlayer==="X" ? "O":"X"

document.getElementById("status").innerText="Player "+currentPlayer+" Turn"

}

}


async function aiMove(){

let response = await fetch("/api/ai_move",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({board})

})

let data = await response.json()

board[data.row][data.col]="X"

renderBoard()

if(checkWinner("X")){
document.getElementById("status").innerText="AI Wins!"
gameOver=true
return
}

if(isDraw()){
document.getElementById("status").innerText="Draw!"
gameOver=true
return
}

currentPlayer="O"

document.getElementById("status").innerText="Player Turn"

}


function checkWinner(player){

for(let i=0;i<3;i++){

if(board[i][0]==player && board[i][1]==player && board[i][2]==player)
return true

if(board[0][i]==player && board[1][i]==player && board[2][i]==player)
return true

}

if(board[0][0]==player && board[1][1]==player && board[2][2]==player)
return true

if(board[0][2]==player && board[1][1]==player && board[1][1]==board[2][0])
return true

return false

}


function isDraw(){

for(let i=0;i<3;i++)
for(let j=0;j<3;j++)
if(board[i][j]==" ")
return false

return true

}


function resetGame(){

startGame(mode,starter)

}