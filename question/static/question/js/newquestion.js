


console.log(initial_input);
// const initial_img_data = initial_input.href;
// const initial_url = URL.createObjectURL(initial_img_data);
imageBox.innerHTML = `<img src="${initial_input.href}" id="image" class="image" width="270px">`;
// imageEditingBox.innerHTML = imageBox.innerHTML;


imageBox.innerHTML = `<img src="${solution_initial_input.href}" id="image" class="image" width="270px">`;
// imageEditingBox.innerHTML = imageBox.innerHTML;



let $inital_image = $('div#image-edit-box .image');

cropperJsView($inital_image);
