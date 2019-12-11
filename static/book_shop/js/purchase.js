const booksForSelling = document.querySelectorAll('.list-group-item-book');
const button = document.getElementById('sell-button');
const amountInput = document.getElementById('sell_amount');
const bookIDInput = document.getElementById('sell_book_id');
let bookChosen = false;

amountInput.addEventListener('change', () => {
    if (bookChosen) {
        button.classList.remove('disabled');
    }
});

booksForSelling.forEach(item => {
    item.addEventListener('click', function () {
        if (amountInput.value !== '') {
            button.classList.remove('disabled');
        }
        bookChosen = true;
        bookIDInput.value = item.attributes['data-book-id'].value;
        booksForSelling.forEach(item => {
            item.classList.remove('bg-success', 'text-light');
        });
        this.classList.add('bg-success', 'text-light');
    });
});

