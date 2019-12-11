function createAlert(status, text) {
    let alert = document.createElement('div');
    alert.classList.add('alert', 'text-center');
    if (status === 'error') {
        alert.classList.add('alert-error');
    } else if (status === 'success') {
        alert.classList.add('alert-success');
    }
    alert.innerText = text;
    return alert;
}


const resolveDeliveryRequest = (listItem) => {
    listItem.classList.remove('bg-light');
    listItem.classList.add('bg-success');
    listItem.classList.add('text-light');
    let textBlock = document.createElement('div');
    textBlock.innerText = 'Заявка выполнена';
    let hr = document.createElement('hr');
    listItem.append(hr);
    listItem.append(textBlock);
};

