        
var shareButton = document.querySelectorAll('a.shareButton');
console.log(shareButton);
function ShareItLite(shareButton){

Array.from(shareButton).forEach(shareBtn => {
    shareBtn.addEventListener('click', e =>{
        // do something
        e.preventDefault();
        if(navigator.share){
            navigator.share({
                title: shareBtn.dataset.title,
                url : shareBtn.dataset.href
            }).catch(console.error);
        }else{
            alert('Use a default share button');
        }
    });
});
}
ShareItLite(shareButton);
$('.DeleteForm').submit(function(e){
    e.preventDefault();
    
    let ans = confirm('This change is permanent\nAre you sure you want to delete this question?');
    if (ans == true){
        const objectBx = $(this).parent().parent().parent();
        serializedData = $(this).serialize();
        $.ajax({
            type: 'POST',
            url : $(this).attr('action'),
            data : serializedData,
            success : function(response){
                objectBx.hide(500);
            },
            error : function(){
                alert('It falis silently!')
            }

        });
    }
});
 



function changed(){
    console.log('This page has changed!')
}



$('.infinite-more-link').click((e)=>{
    e.preventDefault();
    alert('This button was clicked!')
})