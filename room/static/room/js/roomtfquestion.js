


function displayTrueOrFalseQuestion(){
    trueOrFalsePage++;
    QandAPage = 0;
    quizPage = 0;
    fourChoicesPage = 0;
    currentPage = 'trueOrFalsePage';
    if (trueOrFalsePage == 1){
      outputBox = ``;
    }

    fetch(`/room/true-or-false-question/${room_id}?page=${trueOrFalsePage}`)

    .then(function(response){
        return response.json();
     }).then(function(response){
        console.log(response);

      for (let res of response){

       outputBox += `
    <div class="container infinite-container" onchange="changed()">

    <div class="questions  infinite-item">
                  
        <div class="quizItem">
        ${res.trueOrFalseQuestion.question}
        </div>
        `;

        if (res.trueOrFalseQuestion.question_image){
          outputBox +=
          `
          <div class="img-container">
              <div class="img-box">
                  <img src="${res.trueOrFalseQuestion.question_image}" alt="" class="img">
              </div>
          </div>
          `;
        }
        outputBox +=
        `
        

          <div class="inline">

          <div class="attempt">
                  ${res.trueOrFalseQuestion.attempts} attempts
          </div>
          <div class="views">views: ${res.trueOrFalseQuestion.views}</div>

          <div class="average">
              ${res.trueOrFalseQuestion.avgScore}%
          </div>
          <div>
              <span id="seconds" class="duration">
                  ${res.trueOrFalseQuestion.duration_in_seconds}
              </span>
              <span class="secondsName">
                  sec            
              </span>

          </div>

          </div>
        </div>
        </div>
        `;

      }


       saver.innerHTML = outputBox;

       let lastQuestion = Array.from(document.querySelectorAll('.questions')).pop();
        roomObjectObserver.observe(lastQuestion);
    
    }).catch(function(error){
      console.error(error);
    })
    

}