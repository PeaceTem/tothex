


console.log('This js file is working!')





$('.DeleteForm').submit(function(e){
    e.preventDefault();
    const objectBx = $(this).parent().parent().parent();
    serializedData = $(this).serialize();
    $.ajax({
        type: 'POST',
        url : $(this).attr('action'),
        data : serializedData,
        success : function(response){
            objectBx.hide(500);
            // const modal = document.querySelector('div#messageContainerTop');
            // document.querySelector('div.messageContainer').style.visibility = 'visible';
            // modal.hide(3000)

        },
        error : function(){
            alert('It falis silently!')
        }

    });
});
 



function changed(){
    console.log('This page has changed!')
}



$('.infinite-more-link').click((e)=>{
    e.preventDefault();
    alert('This button was clicked!')
})