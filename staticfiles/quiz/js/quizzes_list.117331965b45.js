
$('.likeForm').submit(function(e){
    alert('before');
    e.preventDefault();
const serializeData = $(this).serialize();
alert(serializeData);
const quiz_id = $(this).data('quiz');
alert(quiz_id)
$.ajax({
    type: 'POST',
    url : $(this).data('url'),
    data : serializeData,
    success : function(response){
        alert(response);
        if (response == 'liked'){
            // console.log($(`#likeButton${id}`));
            $(`#likeButton${quiz_id}`).text('unlike');
        }else if (response == 'unliked'){
            // console.log($(`#unlikeButton${id}`));
            $(`#likeButton${quiz_id}`).text('like');
        }
    },
    error : function(){
        alert('It falis silently!')
    }

});
})


