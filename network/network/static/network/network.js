document.addEventListener('DOMContentLoaded', () => {

    //follow/unfollow button
    document.querySelector('#getUserInfo').addEventListener('click', getUserInfo);

})

function getUserInfo(){
    var userID = document.querySelector('#userID').innerHTML;

    //example get request
    fetch(`/users/${userID}`)
    .then(response => response.json())
    .then(user => {
            console.log(user);          
    })
    .catch(error => {
        console.error('error:', error);
    })
}