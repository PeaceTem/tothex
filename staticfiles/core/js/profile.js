const nav = document.querySelector('#navActive');
let navigation = nav.value;
console.log(navigation);

const topNavigation = document.querySelectorAll('.topNavigation');



if (navigation == 'profile'){
    topNavigation[4].classList.add('active');
}