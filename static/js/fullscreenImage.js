   
   var FULLSCREENIMAGES = document.images;
   console.log(FULLSCREENIMAGES);
   
   
   function getFullScreenElement(){
       return document.fullscreenElement
         ||  document.webkitFullscreenElement
         ||  document.mozFullscreenElement
         ||  document.msFullscreenElement;
   }


   function toggleFullScreen(fullscreenDiv){
      if (getFullScreenElement()){
         document.exitFullscreen();
      } else {
         // document.documentElement.requestFullscreen().catch((e)=>{
            fullscreenDiv.requestFullscreen().catch((e)=>{

           console.log(e);
       })
      }
   }
   
   
   
   Array.from(FULLSCREENIMAGES).forEach(FULLSCREENIMAGE =>{
       FULLSCREENIMAGE.addEventListener('click', (e)=>{
           toggleFullScreen(FULLSCREENIMAGE);
       })

   })
