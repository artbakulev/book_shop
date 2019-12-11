const deliveryRequests = document.querySelectorAll('.list-group-item.bg-light[data-request-id]');
deliveryRequests.forEach(item => {
    let button = item.querySelector('button');
    button.addEventListener('click', () => {
        let requestID = item.attributes['data-request-id'].value;
        button.style.display = 'none';
        resolveDeliveryRequest(item);
        sendPost('/api/delivery_requests/', {'request_id': requestID}).catch(e => console.log(e));
    })
});


const requestsForDelivery = document.querySelectorAll('.list-group-item-book');
const button = document.getElementById('worker-delivery-button');
const deliveryModalBody = document.getElementById('delivery-modal-body');
requestsForDelivery.forEach(item => {
    item.addEventListener('click', function () {
        requestsForDelivery.forEach(item => {
            item.classList.remove('bg-success', 'text-light');
        });
        this.classList.add('bg-success', 'text-light');
    });
});

const deliveryAmountInput = document.getElementById('delivery-amount');
button.addEventListener('click', () => {
    let book_id = document.querySelector('.list-group-item-book.bg-success').attributes['data-book-id'].value;
    sendPost('/api/delivery_requests/', {'book_id': book_id, 'amount': deliveryAmountInput.value}).catch(e => console.log(e));
    deliveryModalBody.insertBefore(createAlert('success', 'Заявка на доставку успешно отправлена'),
        deliveryModalBody.firstChild);
});


const supplyRequestBtn = document.getElementById('supply-request-button');
supplyRequestBtn.addEventListener('click', () => {
    let email = document.getElementById('supply-email').value;
    let name = document.getElementById('supply-name').value;
    let phone = document.getElementById('supply-phone').value;
    let book_id = document.querySelector('.list-group-item-book.bg-success').attributes['data-book-id'].value;
    let body = document.getElementById('supply-modal-body');
    sendPost('/api/supply_requests/', {'email': email, 'name': name, 'phone': phone, 'book_id': book_id})
        .then(() => {
                body.insertBefore(createAlert('success', 'Заявка успешно отправлена'), body.firstChild);
            }
        )
});