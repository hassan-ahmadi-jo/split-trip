const participantRemoveEls = document.querySelectorAll('.js-participant-remove');
const expenseRemoveEls = document.querySelectorAll('.js-expense-remove');

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
        el.title = 'This participant cannot be deleted because they have payments or balances.';
    }
    
    
}
participantRemoveEls.forEach(element => participantRemoveHandler(element))


const expenseRemoveHandler = function(el){
    const container = el.closest('.js-expense');
    const shareEl = container.querySelector('.js-share');
    const share = parseFloat(String(shareEl.textContent).replace(/[^\d.]/g, '').replace(/(\..*)\./g, '$1'));
    if (share !== 0) {
        el.disabled = true;
        el.classList.remove('remove-button');
        el.classList.add('remove-botton-disabled');
        el.title = 'This expense cannot be deleted because it has payments.';
    }
    
    
}
expenseRemoveEls.forEach(element => expenseRemoveHandler(element))

