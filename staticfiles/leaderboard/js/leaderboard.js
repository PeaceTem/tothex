const nav = document.querySelector('#navActive');
let navigation = nav.value;
console.log(navigation);

const topNavigation = document.querySelectorAll('.topNavigation');



if (navigation == 'leaderboard'){
    console.log('yes');
    console.log(topNavigation[2])
    topNavigation[2].classList.add('active');
}