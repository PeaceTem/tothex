const nav = document.querySelector('#navActive');
let navigation = nav.value;
console.log(navigation);

const topNavigation = document.querySelectorAll('.topNavigation');



if (navigation == 'questions'){
    topNavigation[1].classList.add('active');
}