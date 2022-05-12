let copyText = document.querySelector(".copy-text");
let urlValue = copyText.querySelector("input.text");
urlValue.value = window.location.href;
copyText.querySelector("button").addEventListener("click",
function(){
    let input = copyText.querySelector("input.text");
    input.select();
    document.execCommand("copy")
    copyText.classList.add("active");
    window.getSelection().removeAllRanges();
    setTimeout(function(){
     copyText.classList.remove("active");
    }, 2500);
});
