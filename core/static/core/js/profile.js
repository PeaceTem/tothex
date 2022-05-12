const nav = document.querySelector('#navActive');
let navigation = nav.value;
console.log(navigation);

const topNavigation = document.querySelectorAll('.topNavigation');



if (navigation == 'profile'){
    topNavigation[3].classList.add('active');
}