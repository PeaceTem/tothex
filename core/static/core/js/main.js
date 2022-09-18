console.log('hello world');
const alertBox = document.getElementById('alert-box');
const imageBox = document.getElementById('image-box');
const imageForm = document.getElementById('image-form');
const confirmBtn = document.getElementById('confirm-btn');
const input = document.getElementById('id_picture');

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
            console.log($imageForm.serialize());
            alert('ajax');
            $.ajax({
                type:'POST',
                url:"",
                enctype: 'multipart/form-data',
                data: fd,
                // data: $imageForm.serialize(),
                success: function(response){
                    console.log('success', response)
                    alertBox.innerHTML = `<div class="alert alert-success" role="alert">
                                            Successfully saved and cropped the selected image
                                        </div>`
                },
                error: function(error){
                    console.log('error', error)
                    alertBox.innerHTML = `<div class="alert alert-danger" role="alert">
                                            Ups...something went wrong
                                        </div>`
                },
                cache: false,
                contentType: false,
                processData: false,
            })
        })
    })
})
