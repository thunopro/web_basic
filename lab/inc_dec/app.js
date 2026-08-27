let counterEl = document.getElementById('counter');
let btnInc = document.getElementById('btn-inc');
let btnDec = document.getElementById('btn-dec');
let btnReset = document.getElementById('btn-reset');

function updateCounter(change) {
    let cnt = parseInt(counterEl.innerText, 10);
    cnt += change;
    counterEl.innerText = cnt;
    if (cnt < 0) {
        counterEl.style.color = 'red';
    } else {
        counterEl.style.color = 'green';
    }
}

function Reset() {
    counterEl.innerText = 0;
    counterEl.style.color = 'green';
}

btnInc.addEventListener('click', () => updateCounter(1));
btnDec.addEventListener('click', () => updateCounter(-1));
btnReset.addEventListener('click', () => Reset());


for ( let i = 0 ; i < 5 ; i ++ ) console.log(i) ; 