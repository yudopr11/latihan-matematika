// const data = document.currentScript.dataset;
const url = document.currentScript.dataset.url
const urlShuffle = document.currentScript.dataset.urlShuffle
const urlFilter = document.currentScript.dataset.urlFilter
var userData;

function capitalizeWords(str) {
    return str.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
};

function updateUserData(quizData) {
    userData = {
        'question': quizData.question,
        'filter': quizData.filter,
        'activeFilter': quizData.activeFilter,
        'currQuestionId': quizData.currQuestionId,
        'score': quizData.score,
        'answerHistory': quizData.answerHistory,
        'progress': quizData.progress, 
        'questionIdTaken': quizData.questionIdTaken,
        'allQuestionId': quizData.allQuestionId,
    };
    return userData;
};

function updateDom(quizData){
    document.querySelector(".progress-bar").style.width = `${quizData.progress*100}%`;

    let allFilter = '';
    for (const key in quizData.filter){
        allFilter += `<div class="filter-option"><h6>${capitalizeWords(key)}</h6><div class="option-list">`
        for (let i in quizData.filter[key]) {
            if (quizData.activeFilter[key].includes(quizData.filter[key][i])) {
                allFilter += `
                <div class="form-check">
                    <input class="form-check-input" type="checkbox" id="${key}-${i}" name="${key}" value="${quizData.filter[key][i]}" checked>
                    <label class="form-check-label" for="${key}-${i}">${quizData.filter[key][i].toUpperCase()}</label>
                </div>`;
            } else {
                allFilter += `
                <div class="form-check">
                    <input class="form-check-input" type="checkbox" id="${key}-${i}" name="${key}" value="${quizData.filter[key][i]}">
                    <label class="form-check-label" for="${key}-${i}">${quizData.filter[key][i].toUpperCase()}</label>
                </div>`;
            }
        };
        allFilter += `</div></div>`;
    };
    document.getElementById("question-filter").innerHTML = allFilter;

    document.getElementById("question-text").innerHTML = quizData.question.text;

    let choices = '';
    if (quizData.question.type == 'pilihan-ganda'){
        for (let key in quizData.question.choices) {
            choices += `<div class="choice-wrapper">
            <input type="radio" class="form-check-input btn-check" name="choices" id="option-${key}" value="${quizData.question.choices[key]}">
            <label class="btn btn-choice" for="option${key}">${key}</label>
            <label for="option-${key}">${quizData.question.choices[key]}</label>
            </div>`;
        };
    } else {
        let i = 0;
        choices += `<div class="table-responsive"><table class="table table-bordered"><thead><tr><th>Pernyataan</th><th class="text-center">Benar</th><th class="text-center">Salah</th></tr></thead><tbody>`;
        for (let key in quizData.question.choices) {
            choices += `<tr>
            <td>
                <input name="choice" id="text-choice-${i}" value="${quizData.question.choices[key]}" type="hidden">${quizData.question.choices[key]}</input>
            </td>
            <td class="text-center align-middle">
                <input class="form-check-input" type="radio" name="choice-${i}" id="choice-${i}" value=true>
            </td>
            <td class="text-center align-middle">
                <input class="form-check-input" type="radio" name="choice-${i}" id="choice-${i}" value=false>
            </td>
            </tr>`;
            i += 1
        };
        choices += `</tbody></table></div>`;
    };
    document.getElementById("question-choices").innerHTML = choices;

    document.getElementById("question-explanation").innerHTML = quizData.question.explanation;
    
    try {
        MathJax.typesetPromise();
    } catch(e) {
        console.log(e)
    };
};

function shuffle(url) {
    let body = updateUserData(userData);

    fetch(url, {
        method: 'post',
        headers: {
            "Content-Type": "application/json; charset=utf-8",
            "mode": "same-origin",
          },
        body : JSON.stringify(body),
        }).then((response) => {
            return response.json()
        }).then((res) => {
            updateDom(res);
            updateUserData(res);
        });
};

window.addEventListener('load', function() {
    function initial(url) {
        fetch(url, {
            method: 'get',
            headers: {
                "Content-Type": "application/json; charset=utf-8",
                "mode": "same-origin",
              }
            }).then((response) => {
                return response.json();
            }).then((res) => {
                updateDom(res);
                updateUserData(res);
            });
    };
    initial(url);
});

document.getElementById("btn-shuffle").addEventListener('click', function () {
    shuffle(urlShuffle);
});

document.getElementById("btn-lanjut").addEventListener('click', function () {
    shuffle(urlShuffle);
    document.querySelector('.alert:not(.hidden)').classList.add('hidden');
    document.getElementById("btn-shuffle").classList.remove('hidden');
    document.getElementById('btn-solution').classList.add('hidden');
    document.getElementById("btn-submit").classList.remove('hidden');
    document.getElementById('btn-lanjut').classList.add('hidden');
    document.getElementById('question-text').scrollIntoView({ block: 'end',  behavior: 'smooth' });
});

// SUBMIT BUTTON
// const btnSubmit = document.getElementById('btn-submit');
// const btnLanjut = document.getElementById('btn-lanjut');
document.getElementById("btn-submit").addEventListener('click', function () {
    document.getElementById("btn-shuffle").classList.add('hidden');
    if (userData.question.explanationType != null && (userData.question.explanation != null || userData.question.explanation != '')) {
        document.getElementById('btn-solution').classList.remove('hidden');
    };
    document.getElementById("btn-submit").classList.add('hidden');
    
    let userChoice;
    let nullCheck = 0;
    if(userData.question.type == 'pilihan-ganda'){
        if (document.querySelector('input[name="choices"]:checked') != null) {
            userChoice = document.querySelector('input[name="choices"]:checked').value
        } else {
            userChoice = null
        };
        const choices = document.querySelectorAll('input[name="choices"]');
        for(let i=0; i<choices.length; i++) {
        choices[i].disabled = true;
        };
    } else {
        userChoice = {}
        for (i = 0; i < document.querySelectorAll('input[name=choice]').length; i++) {
            let key = document.querySelectorAll('input[name=choice]')[i].value;
            let val = null;
            try {
                val = document.querySelector(`input[name=choice-${i}]:checked`).value;
            }
            catch(err) {
                nullCheck += 1;
            };
            userChoice[key] = val;
        document.querySelectorAll(`input[name=choice-${i}]`)[0].disabled = true
        document.querySelectorAll(`input[name=choice-${i}]`)[1].disabled = true
        }; 
        userChoice = JSON.stringify(userChoice);
    };

    let body =  updateUserData(userData);
    body.userAnswer = userChoice
   
    fetch(url, {
    method: 'post',
    headers: {
        "Content-Type": "application/json; charset=utf-8",
        "mode": "same-origin",
      },
    body: JSON.stringify(body),
    }).then((response) => {
        return response.json()
    }).then((res) => {
        if (res.isCorrect) {
            document.getElementById('benar').classList.remove('hidden');
            document.getElementById('benar').scrollIntoView();
        } else if ((res.isCorrect === false && userChoice === null) || (nullCheck == document.querySelectorAll('input[name=choice]').length && userData.question.type == 'tabel-benar-salah')) {
            document.getElementById('kosong').classList.remove('hidden');
            document.getElementById('kosong').scrollIntoView();
        } else {
            document.getElementById('salah').classList.remove('hidden');
            document.getElementById('salah').scrollIntoView();
        };

        if(res.allQuestionId.length == res.questionIdTaken.length){
            document.getElementById('btn-selesai').classList.remove('hidden');
        } else {
            document.getElementById('btn-lanjut').classList.remove('hidden');
        };

        document.querySelector(".progress-bar").style.width = `${res.progress*100}%`;

        updateUserData(res);
    });
});

// FILTER BUTTON
document.getElementById("btn-filter").addEventListener('click', function () {
    const userFilter = {}
    for (key in userData.filter){
        const l = []
        for (const value of document.querySelectorAll(`input[name=${key}]:checked`).values()) {
            l.push(value.value);
        };
        userFilter[key] = l;
    };

    for (key in userFilter){
        if(userFilter[`${key}`].length == 0) {
            userFilter[`${key}`] = userData.filter[`${key}`];
        };
    };

    if(JSON.stringify(userData.activeFilter) != JSON.stringify(userFilter)) {
        let body =  updateUserData(userData);
        body.activeFilter = userFilter;
        fetch(urlFilter, {
            method: 'post',
            headers: {
                "Content-Type": "application/json; charset=utf-8",
                "mode": "same-origin",
                },
            body: JSON.stringify(body),
            }).then((response) => {
                return response.json()
            }).then((res) => {
                if (document.getElementById("btn-submit").classList.contains('hidden')) {
                    document.querySelector('.alert:not(.hidden)').classList.add('hidden');
                    document.getElementById("btn-shuffle").classList.remove('hidden');
                    document.getElementById('btn-solution').classList.add('hidden');
                    document.getElementById("btn-submit").classList.remove('hidden');
                    document.getElementById('btn-lanjut').classList.add('hidden');
                }
                updateDom(res);
                document.getElementById('question-text').scrollIntoView();
                updateUserData(res);
            });
    };
});


// FILTER TOGGLE ANIMATION
// const filter = document.getElementById('filter');
// const filterToggle = document.getElementById('filter-toggle');
document.getElementById('filter').addEventListener('show.bs.offcanvas', function () {
    document.getElementById('filter-toggle').className = 'filter rotated open';
});
document.getElementById('filter').addEventListener('hide.bs.offcanvas', function () {
    document.getElementById('filter-toggle').className = 'filter rotated';
});

// RESET BUTTON & STOP BUTTON ANIMATION
// const btnShuffle = document.getElementById("btn-shuffle");
// const btnStop = document.getElementById('btn-stop');
function removeBtnAni() {
    document.getElementById("btn-shuffle").classList.remove('rotated360');
    document.getElementById('btn-stop').classList.remove("fliped");
}
document.getElementById("btn-shuffle").addEventListener('click', function () {
    document.getElementById("btn-shuffle").classList.add('rotated360');
    setTimeout(removeBtnAni, 500);
})

document.getElementById('btn-stop').addEventListener('click', function () {
    document.getElementById('btn-stop').classList.add('fliped');
    setTimeout(removeBtnAni, 500);
});

// SHOW SOLUTION
// const solPage = document.querySelector('.solution');
// const solClose = document.getElementById('solution-close');
// const solOpen = document.getElementById('btn-solution')
document.getElementById('solution-close').addEventListener('click', function () {
    document.querySelector('.solution').className = 'solution close';
    document.querySelector('.solution').removeChild(document.querySelector('.solution').children[1]);
    document.getElementById('btn-solution').style.backgroundImage = 'url("/static/quiz/image/lightbulb.svg")';
});
document.getElementById('btn-solution').addEventListener('click', function () {
    const backDrop = document.createElement('div');
    backDrop.classList.add('offcanvas-backdrop', 'fade', 'show');
    document.querySelector('.solution').className = 'solution open';
    document.querySelector('.solution').insertAdjacentElement('beforeend', backDrop);
    document.getElementById('btn-solution').style.backgroundImage = 'url("/static/quiz/image/lightbulb-fill.svg")';
});