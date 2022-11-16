const cameraIcons = document.querySelectorAll('.camera-icon');


Array.from(cameraIcons).forEach(icon =>{
    icon.addEventListener('click', ()=>{
        console.log('Hello');
        console.log(icon.previousElementSibling.lastElementChild.lastElementChild);
        let clickableCameraEffect = icon.previousElementSibling.lastElementChild.lastElementChild;
        clickableCameraEffect.click();
        
        // previous
    })
})
