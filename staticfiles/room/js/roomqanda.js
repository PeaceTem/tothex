
function displayQandAPage(){
   QandAPage++;
   quizPage = 0;
   fourChoicesPage = 0;
   trueOrFalsePage = 0;
   currentPage = 'QandAPage';
   if(QandAPage == 1){
      outputBox = ``;
   }

fetch(`/room/question/${room_id}?page=${QandAPage}`)
.then(function(response){
   return response.json();
}).then(function(response){

  outputBox += `
  <div id="question-container" class="infinite-container">      
  `;
  for (let res of response){
     outputBox += `
     
     <div class="question-card infinite-item">
        <a class="question-link" href="add manually">
           <div class="question">${res.question.question}</div>
           <div>${res.question.description}</div>
           <span>${res.question.views} views</span>
           <div>Asked by <b>@${res.question.profile}</b> on ${res.question.date}</div>
        </a>
     </div>
     `;
  }

  outputBox += `
  </div>
  `;
  saver.innerHTML = outputBox;
  let lastQuestion = Array.from(document.querySelectorAll('.question-card')).pop();
   roomObjectObserver.observe(lastQuestion);

}).catch(function(error){
  console.error(error);
})


}
