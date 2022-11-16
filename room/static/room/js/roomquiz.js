

function displayQuizPage(){
   quizPage++;
   QandAPage = 0;
   fourChoicesPage = 0;
   trueOrFalsePage = 0;
   currentPage = 'quizPage';
   if (quizPage == 1){
      outputBox = ``;
   }
    fetch(`/room/quiz/${room_id}?page=${quizPage}`)
    .then(function(response){
       return response.json();
    }).then(function(response){


       for (let res of response){
          outputBox += `
          <div class='card infinite-item'>
             <div class="contentBx">
                <a href="add the link manaually" class="username">
                      <img src="https://picsum.photos/300" alt="">
                      @${res.quiz.user.username}
                </a>
                <div class="categories">
 
          ` ;
 
                   
          for (let category of res.quiz.categories){
             outputBox += 
 
             `
             <div class="category">
                   <a href="add manually">
                         ${category.title}
                   </a>
             </div>
             `;
          }
          
          outputBox += 
 
          `
          </div>
          <div id="outputDate" class="outputDate">${res.quiz.date}</div>
          <div class="title-block">`;
 
 
       if (`{{profile}}`){
       outputBox +=
 
          `
          <a class="link" href="add manually">
          `
       } else{
       outputBox +=
 
          `
          <a class="link" href="add manually">
          
          `
       }
       outputBox +=
 
                `
                <img src="https://picsum.photos/600/360" alt="">
                <div class="title">
                   ${res.quiz.title}
                </div>
             </a>
          </div>
 
 
                   <div class="desc">
                      ${res.quiz.description}
                </div>
                <div class="inline inlineOne">
                      
                      <div style="color:#999;" class="questionLength">
                         questions: ${res.quiz.questionLength}
                      </div>
                      
                      <div style="color:#999;" class="duration">
                         ${res.quiz.get_duration}
                      </div>
 
                </div>
                <div style="color:#999;" class="inline inlineTwo">
                      <div style="color:#999;" class="attempt">
                         attempts: ${res.quiz.attempts}
                      </div>
                      <div style="color:#999;" class="average">
                         ${res.quiz.average_score}%
                      </div>
                      <div style="color:#999;">
                         ${res.quiz.age_from} to ${res.quiz.age_to} years
                      </div>
                </div>
                         <div class="linkBx">
                         <div id="likes">
                      <span>likes: ${res.quiz.likeCount}</span>
                            
                         </div>
                         <div id="take-quiz">
                            <a class="link" href="add manually"><div>Take Quiz →</div></a>
                         </div>
                         </div>
                         
             </div>
          </div>
          `;
 
       }
       saver.innerHTML = outputBox;
          //  let lastQuiz = Array.from(document.get).forEach(q =>{
    let lastQuiz = Array.from(document.querySelectorAll('.card')).pop();
   //  let counterr = Array.from(lastQuiz).pop();
   //  });

   //  lastQuiz = lastQuiz[lastQuiz.length - 1]
    console.log(lastQuiz);
   //  console.log(counterr);
    roomObjectObserver.observe(lastQuiz);
    }).catch(function(error){
       console.error(error);
    })

 }
 
