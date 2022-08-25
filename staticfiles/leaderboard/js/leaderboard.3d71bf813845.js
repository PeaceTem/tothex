const nav = document.querySelector('#navActive');
let navigation = nav.value;
console.log(navigation);

const topNavigation = document.querySelectorAll('.topNavigation');



if (navigation == 'leaderboard'){
    console.log('yes');
    console.log(topNavigation[3])
    topNavigation[3].classList.add('active');
}