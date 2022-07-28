


console.log('This js file is working!')





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