console.log('hello world');
// const alertBox = document.getElementById('alert-box');
const imageBox = document.getElementById('image-box');
const solutionImageBox = document.getElementById('solution-image-box');
// const questionForm = document.getElementById('question-form');
// const confirmBtn = document.getElementById('confirm-btn');
const input = document.getElementById('id_question_image');
const solution_input = document.getElementById('id_solution_image');



const csrf = document.getElementsByName('csrfmiddlewaretoken');

const imageOverlay = document.querySelector("#image-overlay");
const cancelButton = document.querySelector('#cancel-edit');
const saveButton = document.querySelector('#save-edit');
const imageEditingBox = document.querySelector('#image-edit-box');
const questionImageEdit = document.querySelector('div#absolute');
const solutionImageEdit = document.querySelector('div#solution-absolute');



const initial_input = document.querySelector('#div_id_question_image div a');
const solution_initial_input = document.querySelector('#div_id_solution_image div a');
if (initial_input){
    // reload_js("{% static 'question/js/newquestion.js' %}?{{static_request}}");
    imageBox.innerHTML = `<img src="${initial_input.href}" id="image" class="image questionImage" width="270px">`;
}

if(solution_initial_input){
    solutionImageBox.innerHTML = `<img src="${solution_initial_input.href}" id="image" class="image solutionImage" width="270px">`;
}
function reload_js(src) {
    $('<script>').attr('src', src).appendTo('head');
}




function cropperJsView(image){
    image.cropper({
        aspectRatio: 0 / 9,
        crop: function(event) {
            console.log(event.detail.x);
            // console.log(event.detail.y);
            // console.log(event.detail.width);
            // console.log(event.detail.height);
            // console.log(event.detail.rotate);
            // console.log(event.detail.scaleX);
            // console.log(event.detail.scaleY);
        }
    });
    cropper= image.data('cropper');

}


// xmlHTTP return blob response
function getImgURL(url, callback){
    var xhr = new XMLHttpRequest();
    xhr.onload = function(){
        callback(xhr.response)
        console.log("It worked 2!");

    };
    xhr.open('GET', url);
    xhr.responseType = 'blob';
    xhr.send();
    console.log("It worked!");
}

var cropper;
var file;
var container;
var $image;








questionImageEdit.addEventListener('click', ()=>{
    imageEditingBox.innerHTML = imageBox.innerHTML;

    imageOverlay.classList.toggle('inactive-overlay');
    
    $image = $('div#image-edit-box .image');
    // let $image = $('#image');
    // change the name of choose file to change image
    cropperJsView($image);

});



solutionImageEdit.addEventListener('click', ()=>{
    imageEditingBox.innerHTML = solutionImageBox.innerHTML;

    imageOverlay.classList.toggle('inactive-overlay');
    
    $image = $('div#image-edit-box .image');
    // let $image = $('#image');
    // change the name of choose file to change image
    cropperJsView($image);

});





cancelButton.addEventListener('click', ()=>{
    imageOverlay.classList.toggle('inactive-overlay');
})




input.addEventListener('change', ()=>{
    // alertBox.innerHTML = "";
    // confirmBtn.classList.remove('not-visible');
    const img_data = input.files[0];
    const url = URL.createObjectURL(img_data);
    // remove the size of the image here 
    // and declare it from the css file
    imageBox.innerHTML = `<img src="${url}" id="image" class="image questionImage" width="270px">`;
    getImgURL(url, (imgBlob)=>{
        // get the name of the original file and add the username in front of it.
        file = new File([imgBlob], 'TheTest.jpeg', {type:"image/jpeg", lastModified: new Date().getTime()}, 'utf-8');
        container = new DataTransfer();
        container.items.add(file);
        input.files = container.files; 
    })

})



solution_input.addEventListener('change', ()=>{
    // alertBox.innerHTML = "";
    // confirmBtn.classList.remove('not-visible');
    const solution_img_data = solution_input.files[0];
    const solution_url = URL.createObjectURL(solution_img_data);
    // remove the size of the image here 
    // and declare it from the css file
    solutionImageBox.innerHTML = `<img src="${solution_url}" id="image" class="image solutionImage" width="270px">`;
    getImgURL(solution_url, (imgBlob)=>{
        // get the name of the original file and add the username in front of it.
        file = new File([imgBlob], 'TheTestSolution.jpeg', {type:"image/jpeg", lastModified: new Date().getTime()}, 'utf-8');
        container = new DataTransfer();
        container.items.add(file);
        solution_input.files = container.files; 
    })

})

var questionTestImage;
var solutionTestImage;
var Imgurl;
var img_url_data;

saveButton.addEventListener('click', ()=>{
    cropper.getCroppedCanvas().toBlob((blob) => {
        console.log('confirmed')
        file = new File([blob], 'TheTestOne1.jpeg', {type:"image/jpeg", lastModified: new Date().getTime()}, 'utf-8');
        container = new DataTransfer();
        container.items.add(file);

        questionTestImage = document.querySelector('#image-edit-box .questionImage');
        solutionTestImage = document.querySelector('#image-edit-box .solutionImage');
        if(questionTestImage){
            // 1
            input.files = container.files; 
            // 1
            img_url_data = input.files[0];
            Imgurl = URL.createObjectURL(img_url_data);

            // remove the size of the image here 
            // and declare it from the css file
            // 1
            imageBox.innerHTML = `<img src="${Imgurl}" id="image" class="image questionImage" width="270px">`;
        }
        else if(solutionTestImage){
            // 1
            solution_input.files = container.files; 
            // 1
            img_url_data = solution_input.files[0];
            Imgurl = URL.createObjectURL(img_url_data);

            // remove the size of the image here 
            // and declare it from the css file
            // 1
            solutionImageBox.innerHTML = `<img src="${Imgurl}" id="image" class="image solutionImage" width="270px">`;   
        }

    })
    imageOverlay.classList.toggle('inactive-overlay');

})




// The solution part








