let samples = [
    { id: 1, name: "A", result: 80 },
    { id: 2, name: "B", result: 45 },
    { id: 3, name: "C", result: 90 }
];

let filtered = [];
for (let i = 0; i < samples.length; i++) {
    if (samples[i].result > 50) {
        filtered.push(samples[i]);
    }
}

function sumResult(arr) {
    let total = 0;
    for (let i = 0; i < arr.length; i++) {
        total += arr[i].result;
    }
    return total;
}

function findMax(arr) {
    let max = arr[0];
    for (let i = 1; i < arr.length; i++) {
        if (arr[i].result > max.result) {
            max = arr[i];
        }
    }
    return max;
}

const sumResultArrow = (arr) => {
    let total = 0;
    for (let i = 0; i < arr.length; i++) {
        total += arr[i].result;
    }
    return total;
};


let sum = sumResult(filtered); 
console.log(sum);

let Max = findMax(filtered);
console.log(Max); 