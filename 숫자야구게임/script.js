const attempts = document.querySelector("#attempts");
const btn = document.querySelector(".submit-button");
const num1 = document.querySelector("#number1");
const num2 = document.querySelector("#number2");
const num3 = document.querySelector("#number3");
const resultsDisplay = document.querySelector("#results");
const resultImg = document.querySelector("#game-result-img");


let re_attempts = 9;
let answer = [];
let user_answer=[];
let gameHistory = [];


function initGame()
{
    re_attempts = 9;
    answer=[];
    while(answer.length<3)
    {
        let random_answer = Math.floor(Math.random()*10);
        if (!answer.includes(random_answer)) 
        {
            answer.push(random_answer);
        }
    }
    num1.value = ""; num2.value = ""; num3.value = "";
}

btn.addEventListener("click", check_number);


function check_number()
{
    if(num1.value ==='' || num2.value ==='' || num3.value ===''){
        alert("값이 입력되지 않았습니다")
        num1.value = ""; num2.value = ""; num3.value = "";
        attempts--;
        return;
    }

    user_answer = [Number(num1.value), Number(num2.value), Number(num3.value)];

    let score =
    {   
        strike : 0,
        ball : 0,
        out : false
    };

    for (let i = 0; i < 3; i++) 
        {
            if (user_answer[i] === answer[i]) 
            {
                score.strike++;
            } 
            else if (answer.includes(user_answer[i])) 
            {
                score.ball++;
            }
        }

    if (score.ball === 0 && score.strike === 0)
    {
        score.out = true;
    }

    let resultText = '';
    if (score.out) 
    {
        resultText = 'OUT';
    } 
    else 
    {
        resultText = `${score.strike}S ${score.ball}B`;
    }

    gameHistory.push({
    input: user_answer.join(' '),
    strike: score.strike,
    ball: score.ball,
    out: score.out
});
    renderHistory();
    re_attempts--;
    attempts.textContent = re_attempts;
    if (score.strike === 3) 
    {
        resultImg.src = './success.png';
        btn.disabled = true;
    } else if (re_attempts <= 0) 
    {
        resultImg.src = './fail.png';
        btn.disabled = true;
    }

    num1.value = ""; num2.value = ""; num3.value = "";
}

function renderHistory() {
    resultsDisplay.innerHTML = ''; 
    
    gameHistory.forEach(item => {
        const resultLine = document.createElement('div');
        resultLine.className = 'check-result'; 
        
        const leftSpan = document.createElement('span');
        leftSpan.className = 'left';
        leftSpan.textContent = item.input;
        
        const centerSpan = document.createElement('span');
        centerSpan.textContent = ':';
        
        const rightSpan = document.createElement('span');
        rightSpan.className = 'right';
        
        if (item.out) {
            rightSpan.innerHTML = `<span class="num-result out">OUT</span>`;
        } else {
            let strikeHTML = '';
            let ballHTML = '';
            
            if (item.strike > 0) {
                strikeHTML = `<span>${item.strike} <span class="num-result strike">S</span></span>`;
            }
            if (item.ball > 0) {
                ballHTML = `<span>${item.ball} <span class="num-result ball">B</span></span>`;
            }
            
            rightSpan.innerHTML = `${strikeHTML} ${ballHTML}`.trim();
        }
        
        resultLine.appendChild(leftSpan);
        resultLine.appendChild(centerSpan);
        resultLine.appendChild(rightSpan);
        
        resultsDisplay.appendChild(resultLine);
    });
}

window.onload = initGame;