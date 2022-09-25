console.log('hello world');
const alertBox = document.getElementById('alert-box');
const imageBox = document.getElementById('image-box');
const imageForm = document.getElementById('image-form');
const confirmBtn = document.getElementById('confirm-btn');
const input = document.getElementById('id_picture'); // change this part to id_solution_picture

const csrf = document.getElementsByName('csrfmiddlewaretoken');

input.addEventListener('change', ()=>{
    alertBox.innerHTML = "";
    confirmBtn.classList.remove('not-visible');
    const img_data = input.files[0];
    const url = URL.createObjectURL(img_data);
    // const width = window.innerWidth;
    imageBox.innerHTML = `<img src="${url}" id="image" width="270px">`;
    var $image = $('#image');
    console.log($image);

    $image.cropper({
        aspectRatio: 0 / 9,
        crop: function(event) {
            console.log(event.detail.x);
            console.log(event.detail.y);
            console.log(event.detail.width);
            console.log(event.detail.height);
            console.log(event.detail.rotate);
            console.log(event.detail.scaleX);
            console.log(event.detail.scaleY);
        }
    });
    
    var cropper = $image.data('cropper');
    confirmBtn.addEventListener('click', ()=>{
        cropper.getCroppedCanvas().toBlob((blob) => {
            console.log('confirmed')
            const fd = new FormData();
            fd.append('csrfmiddlewaretoken', csrf[0].value)
            // fd.append('file', blob, 'my-image.png');
            fd.append('picture', blob, 'my-image.png');
            const $imageForm = $('#image-form');
        })
    })
})
/*
Get the cropped data and assign it to the value of picture form data using js
Add an alert box to show that it has been saved to the picture form data.
Insert the alert box above the picture form box and solution form box

get the size of the cropped data and compress it for storage purpose

*/