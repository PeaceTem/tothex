


function displayFourChoicesQuestion(){
    currentPage = 'fourChoicesPage';
    fourChoicesPage++;
    quizPage = 0;
    trueOrFalsePage = 0;
    QandAPage = 0;
    if(fourChoicesPage == 1){
      outputBox = ``;
    }
    fetch(`/room/four-choices-question/${room_id}?page=${fourChoicesPage}`)

    .then(function(response){
        return response.json();
     }).then(function(response){
        console.log(response);

      for (let res of response){

       outputBox += `
    <div class="container infinite-container" onchange="changed()">

    <div class="questions  infinite-item">
                  
        <div class="quizItem">
        ${res.fourChoicesQuestion.question}
        </div>
        `;

        if (res.fourChoicesQuestion.question_image){
          outputBox +=
          `
          <div class="img-container">
              <div class="img-box">
                  <img src="${res.fourChoicesQuestion.question_image}" alt="" class="img">
              </div>
          </div>
          `;
        }
        outputBox +=
        `
        

          <div class="inline">

          <div class="attempt">
                  ${res.fourChoicesQuestion.attempts} attempts
          </div>
          <div class="views">views: ${res.fourChoicesQuestion.views}</div>

          <div class="average">
              ${res.fourChoicesQuestion.avgScore}%
          </div>
          <div>
              <span id="seconds" class="duration">
                  ${res.fourChoicesQuestion.duration_in_seconds}
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

