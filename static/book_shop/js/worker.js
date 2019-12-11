const listItems = document.querySelectorAll('.list-group-item.bg-light[data-request-id]');
listItems.forEach(item => {
    let button = item.querySelector('button');
    button.addEventListener('click', () => {
        let requestID = item.attributes['data-request-id'].value;
        button.style.display = 'none';
        makeActive(item);
        let err = sendPost('/api/delivery_requests/', {'request_id': requestID});
    })
});

const makeActive = (listItem) => {
    listItem.classList.remove('bg-light');
    listItem.classList.add('bg-success');
    listItem.classList.add('text-light');
    let textBlock = document.createElement('div');
    textBlock.innerText = 'Заявка выполнена';
    let hr = document.createElement('hr');
    listItem.append(hr);
    listItem.append(textBlock);
};

const listBookItems = document.querySelectorAll('.list-group-item-book');
listBookItems.forEach(item => {
    item.addEventListener('click', function () {
        listBookItems.forEach(item => {
            item.classList.remove('bg-success');
            item.classList.remove('text-light');
        });
        this.classList.add('bg-success');
        this.classList.add('text-light');
    });
    //TODO: доделай тут
    let button = item.querySelector('button');
    button.addEventListener('click', () => {
        let requestID = item.attributes['data-request-id'].value;
        button.style.display = 'none';
        makeActive(item);
        let err = sendPost('/api/delivery_requests/', {'request_id': requestID});
    })
});