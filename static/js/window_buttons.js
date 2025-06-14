// Window Buttons
const btnClose = document.getElementById('btn_close');

btnClose.addEventListener('click', (event) => {
    event.preventDefault();

    window.location.href = '/';
});