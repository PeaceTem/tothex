const nav = document.querySelector('#navActive');
let navigation = nav.value;
console.log(navigation);

const all = document.querySelector('#all');
const following = document.querySelector('#following');
const my = document.querySelector('#my');
const topNavigation = document.querySelectorAll('.topNavigation');



if (navigation == 'quizzes'){
    all.classList.add('active')
    topNavigation[0].classList.add('active');
}else if (navigation == 'following-quizzes'){
    following.classList.add('active')
    topNavigation[0].classList.add('active');
}else if (navigation == 'my-quizzes'){
    my.classList.add('active')
    topNavigation[0].classList.add('active');
}



let dates = document.querySelectorAll('div.date');
console.log(dates)
let dateValues =[]
for (var dateCounter of dates){
    console.log('yes')
    dateValues.push(dateCounter.textContent);
}



function convert(d){
    
let date = new Date(d);
// console.log(date);
let now = new Date();
// console.log(now);
diff = now - date
// console.log(diff);
sec = Math.round(diff/1000);
min = Math.round(sec/60);
hour = Math.round(min/60);
days = Math.round(hour/24);
weeks = Math.round(days/7);
months = Math.round(days/30);
years = Math.round(days/365);
// console.log(`${sec} seconds`);
// console.log(`${min} minutes`);
// console.log(`${hour} hours`);
// console.log(`${days} days`);

let outputDate;
if(months > 0){
    outputDate = `${months} months`
}else if (weeks > 0){
    outputDate = `${weeks} weeks`
}else if (days > 0){
    outputDate = `${days} days`
}else if(hour > 0){
    outputDate = `${hour} hours`
}else if(min > 0){
    outputDate = `${min} min`
}else if(hours > 0){
    outputDate = `${sec} sec`
}

return outputDate;
}


let output = document.querySelectorAll('.outputDate');
console.log(output.length);
dateValues.forEach((e)=>{
    console.log(convert(e));
})

for(var dateContent = 0; dateContent < parseInt(output.length); dateContent++){
    output[dateContent].textContent = convert(dateValues[dateContent]);
}

// console.log(dateValues)
// console.log(dates[0].textContent);

// let datepoint = document.getElementById('outputDate');
// datepoint.textContent = outputDate;
// console.log(outputDate);




function likeFunction(value){
    let likeObject = document.getElementById(value);
    console.log(likeObject);
    $(document).on('submit', likeObject.parentNode, function(e){
        alert('JQuery is working!');
        e.preventDefault();
        // alert($(`#${value}`).data('url'));

        $.ajax({
            type: 'GET',
            url : $(`#${value}`).parent().data('url'),
            data : {
                quiz_id: $(`#${value}`).parent().data('quiz'),
            },
            success : function(response){
                alert('It works');
                // document.querySelector('#deleteButton').parentNode.parentNode.style.display = 'none';
                const id =$(`#${value}`).parent().data('quiz');
                // console.log(id);
                // console.log(response)
                if (response == 'liked'){
                    // console.log($(`#likeButton${id}`));
                    $(`#unlikeButton${id}`).text('unlike');
                }else if (response == 'unliked'){
                    // console.log($(`#unlikeButton${id}`));
                    $(`#unlikeButton${id}`).text('like');
                }
                

            },
            error : function(){
                alert('It falis silently!')
            }

        });
    });
        

}









