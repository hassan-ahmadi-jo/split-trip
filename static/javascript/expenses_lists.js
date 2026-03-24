const participantRemoveEls = document.querySelectorAll('.js-participant-remove');

const participantRemoveHandler = function(el){
    const container = el.closest('.js-participant');
    const paidEl = container.querySelector('.js-paid');
    const shareEl = container.querySelector('.js-share');
    const paid = parseFloat(String(paidEl.textContent).replace(/[^\d.]/g, '').replace(/(\..*)\./g, '$1'));
    const share = parseFloat(String(shareEl.textContent).replace(/[^\d.]/g, '').replace(/(\..*)\./g, '$1'));
    if (paid + share !== 0) {
        el.disabled = true;
        el.classList.remove('remove-button');
        el.classList.add('remove-botton-disabled');
        el.title = 'Cannot delete a participant who has payments or balances.';
    }
    
    
}
participantRemoveEls.forEach(element => participantRemoveHandler(element))

