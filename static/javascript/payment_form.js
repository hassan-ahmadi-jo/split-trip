const amountEls = document.querySelectorAll('.js-amount');
const cost = document.querySelectorAll('.cost');
const amountCommentBtns = document.querySelectorAll('.js-amount-comment-btn');
const amountCommentEls = document.querySelectorAll('.js-amount-comment');
const paidAmountEls = document.querySelectorAll('.js-paid-amount');
const totalAmountEls = document.getElementById('total-amounts');
const totalpaidAmountEls = document.getElementById('total-paid-amounts');
const formEl = document.getElementById('form');
const payerBtns = document.querySelectorAll('.js-payer-btn');

// Cost Handler

// Format numbers (e.g., 12345.6789 → 12,345.67)
// Remove non-numeric characters from input (e.g., 12a3 → 123)
const costHandler = function (text) {
    let number = String(text).replace(/[^\d.]/g, '').replace(/(\..*)\./g, '$1');
    if (number.length > 13) {
        number = number.slice(0, 13);
    };
    if (number == '0.00') {
        number = ''
    }
    dot_index = number.indexOf('.');
    let integer_part = '';
    let decimal_part = '';

    if (dot_index == -1) {
        integer_part = number;
    } else {
        integer_part = number.slice(0, dot_index);
        decimal_part = number.slice(dot_index + 1);
    }

    let formatted_integer_part = '';
    int_len = integer_part.length;
    for (i in integer_part) {
        if ((int_len - i) % 3 == 0 & i != 0) {
            formatted_integer_part += ',';
        };
        formatted_integer_part += integer_part[i];
    }
    let cost_number = ''
    if (dot_index == -1) {
        cost_number = formatted_integer_part;
    } else if (number.length - dot_index == 1) {
        cost_number = formatted_integer_part + '.';
    } else {
        cost_number = formatted_integer_part + '.' + decimal_part.slice(0, 2);
    }
    return cost_number;
};
// End Cost Handler

// -----------------------------
// Function to check the financial balance and update the header color. #AI
var total_shares = 0;
var total_paid = 0;
function updateBalanceUI(totalShares, totalPaid) {
    const indicator = document.getElementById('balance-indicator');
    const statusText = document.getElementById('status-text');
    const paidCard = document.querySelector('.js-balance-card');
    const paidValue = document.querySelector('#total-paid-amounts');
    const submitBtn = document.getElementById('submit-btn');
    const not_equal_error = document.getElementById('not-equal-error')
    const need_payer_error = document.getElementById('need-payer-error')
    
    const isBalanced = (totalShares === totalPaid);

    if (isBalanced) {
        indicator.classList.remove('bg-red-500/10', 'border-red-500/20', 'text-red-500');
        indicator.classList.add('bg-emerald-500/20', 'border-emerald-500/40', 'text-emerald-400');
        statusText.innerText = "Balanced";

        paidCard.classList.add('border-emerald-500/40', 'bg-emerald-500/5');
        paidValue.classList.replace('text-white', 'text-emerald-400');


        submitBtn.disabled = false;
        submitBtn.classList.add('sunmit-button-active');
        submitBtn.classList.remove('sunmit-button-not-active');
        not_equal_error.classList.add('hidden');
        need_payer_error.classList.add('hidden');

    } else {
        indicator.classList.remove('bg-emerald-500/20', 'border-emerald-500/40', 'text-emerald-400');
        indicator.classList.add('bg-red-500/10', 'border-red-500/20', 'text-red-500');
        statusText.innerText = "Not Balanced";

        paidCard.classList.remove('border-emerald-500/40', 'bg-emerald-500/5');
        paidValue.classList.replace('text-emerald-400', 'text-white');

        submitBtn.disabled = true;
        submitBtn.classList.remove('sunmit-button-active');
        submitBtn.classList.add('sunmit-button-not-active');
        not_equal_error.classList.remove('hidden');
        need_payer_error.classList.add('hidden');
        if (totalPaid == '0'){
            need_payer_error.classList.remove('hidden');
        };

    }
}


// -----------------------------
// Total Amount Handler
// Calculate the total amount and update the UI
const totalAmountsHandler = function (el) {
    let sum = 0
    amountEls.forEach(el => {
        const number = parseFloat(el.value.replace(/[^\d.]/g, ''))
        if (number) {
            sum += number;
        }
    });

    if (sum) {
        totalAmountEls.innerText = costHandler(sum);
        total_shares = sum;
    } else {
        totalAmountEls.innerText = '0'
        total_shares = 0;
    };
    updateBalanceUI(total_shares, total_paid);
};
// End Total Amount Handler

// -----------------------------
// Total Paid Amount Handler
// Calculate the total paid amount and update the UI
const totalPaidAmountsHandler = function (el) {
    let sum = 0
    paidAmountEls.forEach(el => {
        const number = parseFloat(el.value.replace(/[^\d.]/g, ''))
        if (number) {
            sum += number;
        }
    });

    if (sum) {
        totalpaidAmountEls.innerText = costHandler(sum);
        total_paid = sum;
    } else {
        totalpaidAmountEls.innerText = '0';
        total_paid = 0;
    };
    updateBalanceUI(total_shares, total_paid);
};
// End Total Paid Amount Handler

// -----------------------------
// Amount Handler

// Update the class list
// Apply the Cost Handler function to amount fields
// Apply Total Amounts Handler function 
const amountHandler = function (el) {
    let value = el.value;
    if (value === '') {
        el.classList.add('amount-input');
        el.classList.remove('amount-input-entered');
    } else {
        el.classList.remove('amount-input');
        el.classList.add('amount-input-entered');

        el.value = costHandler(value);
    }
    totalAmountsHandler(el);
};
amountEls.forEach(element => {
    element.addEventListener('input', el => amountHandler(el.target));
    amountHandler(element);
});
// End Amount Handler

// -----------------------------
// Amount Paid Handler

// Update the class list
// Apply the Cost Handler function to amount paid fields
// Apply Total Amounts paid Handler function 
const paidAmountHandler = function (el) {
    let value = el.value;
    if (value === '') {
        el.classList.add('amount-paid-input');
        el.classList.remove('amount-paid-input-entered');
    } else {
        el.classList.remove('amount-paid-input');
        el.classList.add('amount-paid-input-entered');

        el.value = costHandler(value);
    }
    totalPaidAmountsHandler(el);
};
paidAmountEls.forEach(element => {
    element.addEventListener('input', el => paidAmountHandler(el.target));
    paidAmountHandler(element);
});
// End Amount Handler

// -----------------------------
// Comment handling
const commentInputHandler = function (el) {
    let value = el.value;
    if (value === '') {
        el.classList.add('wizard-input');
        el.classList.remove('amount-input-entered');
    } else {
        el.classList.remove('wizard-input');
        el.classList.add('amount-input-entered');
    }
};
amountCommentEls.forEach(element => {
    element.addEventListener('input', el => commentInputHandler(el.target));
    commentInputHandler(element);
});

const commentFocusHandler = function (el) {
    const container = el.parentElement;
    const btn = container.querySelector('.js-amount-comment-btn')

    let value = el.value;
    if (value === '') {
        el.classList.add('hidden');
        btn.classList.remove('hidden');
    } else {
        el.classList.remove('hidden');
        btn.classList.add('hidden');
    }
};
amountCommentEls.forEach(element => {
    element.addEventListener('blur', el => commentFocusHandler(el.target));
    commentFocusHandler(element);
});

const commentBtnHandler = function (el) {
    const container = el.parentElement;
    const textArea = container.querySelector('.js-amount-comment')
    el.classList.add('hidden')
    textArea.classList.remove('hidden')
};
amountCommentBtns.forEach(element => { element.addEventListener('click', el => commentBtnHandler(el.target)) });
// End Comment handling


// -----------------------------
// Form submit
const formHandler = function () {
    amountEls.forEach(element => {
        element.value = element.value.replace(/[^\d.]/g, '');
        if (element.value === '') {
            element.value = 0;
        }
    });
    paidAmountEls.forEach(element => {
        element.value = element.value.replace(/[^\d.]/g, '');
        element.classList.remove('hidden');
        if (element.value === '') {
            element.value = 0;
        }
    });
};
formEl.addEventListener('submit', formHandler);
// End Form submit

// -----------------------------
// Handle payer and non-payer buttons. AI
const togglePayerStatus = function (el, status) {
    const container = el.closest('.js-participant-card');
    const payerBtn = container.querySelector('.js-payer-btn');
    const nonPayerBtn = container.querySelector('.js-non-payer-btn');
    const payerBadge = container.querySelector('.js-payer-badge');
    const payerFild = container.querySelector('#payer-fild');
    const paidAmountEl = container.querySelector('.js-paid-amount');



    if (status === 'payer') {

        payerBtn.classList.add('bg-emerald-600', 'text-white', 'shadow-lg');
        payerBtn.classList.remove('text-gray-500');
        nonPayerBtn.classList.remove('bg-gray-800', 'text-cyan-400', 'shadow-sm');
        nonPayerBtn.classList.add('text-gray-500');


        container.classList.add('border-emerald-500/50', 'bg-emerald-500/5');
        container.classList.remove('bg-gray-900/40', 'border-gray-700/50');


        payerBadge.classList.remove('hidden');



        payerFild.classList.remove('hidden')
    } else {

        nonPayerBtn.classList.add('bg-gray-800', 'text-cyan-400', 'shadow-sm');
        nonPayerBtn.classList.remove('text-gray-500');
        payerBtn.classList.remove('bg-emerald-600', 'text-white', 'shadow-lg');
        payerBtn.classList.add('text-gray-500');

        container.classList.remove('border-emerald-500/50', 'bg-emerald-500/5');
        container.classList.add('bg-gray-900/40', 'border-gray-700/50');

        payerBadge.classList.add('hidden');

        payerFild.classList.add('hidden');
        paidAmountEl.value = '';
        paidAmountEls.forEach(element => paidAmountHandler(element));
    }
};


// Initialize elements handler
// Handle number display formatting
// Select the payer if the participant is marked as a payer
payerBtns.forEach(element => {
    const container = element.closest('.js-participant-card');
    const paidAmountEl = container.querySelector('.js-paid-amount');
    const amountEl = container.querySelector('.js-amount');
    const amount_value = amountEl.value;
    const paid_value = paidAmountEl.value;

    if (paid_value === '' || paid_value === '0' || paid_value === '0.00') {
        paidAmountEl.value = '';
    } else {
        element.click();
    };

    if (amount_value === '0' || amount_value === '0.00') {
        amountEl.value = '';
    };

    if (amount_value.slice(-3) == '.00'){
        amountEl.value = amount_value.slice(0, -3);
    }

    if (paid_value.slice(-3) == '.00'){
        paidAmountEl.value = paid_value.slice(0, -3);
    }




    paidAmountEl.removeAttribute('required');
    paidAmountEl.required = false;

    amountEl.removeAttribute('required');
    amountEl.required = false;
});
