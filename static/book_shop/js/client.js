const btn = document.querySelector('#client-btn');
const form = document.getElementById('modal-body');
const emailInput = document.getElementById('email');
const nameInput = document.getElementById('name');
const phoneInput = document.getElementById('phone');
const bookIDInput = document.getElementById('book_id');
btn.addEventListener('click', () => {
    sendPost('/api/supply_requests/', {
        "email": emailInput.value,
        "name": nameInput.value,
        "phone": phoneInput.value,
        "book_id": bookIDInput.value
    })
        .then(() => {
                form.innerHTML = 'Заявка отправлена, мы с вами свяжемся!';
            }
        )
        .catch(() => {
            form.innerHTML = 'Произошла ошибка. Повторите позднее';

        });
    btn.style.display = 'none';

});