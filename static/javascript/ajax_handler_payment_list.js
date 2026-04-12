// AJAX
const ajaxContainerEls = document.querySelectorAll('.js-ajax-container');

ajaxContainerEls.forEach(function (container) {
    const ajaxForms = container.querySelectorAll('.js-ajax-form');
    const joinRequestFormHandler = function (element) {

        element.addEventListener('submit', function (el) {
            el.preventDefault();
            formData = new FormData(this);
            formData.append(el.submitter.name, el.submitter.value);
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            url = this.action;
            fetch(url, {
                method: 'POST',
                headers: { "X-CSRFToken": csrfToken },
                body: formData
            }).then(
                response => response.text()
            ).then(
                htmlData => {
                    container.innerHTML = htmlData;

                    const newajaxForms = document.querySelectorAll('.js-ajax-form');
                    newajaxForms.forEach(form => joinRequestFormHandler(form));
                    
                    const newPriceEls = document.querySelectorAll('.js-price')
                    newPriceEls.forEach(element => element.textContent = formatPrice(element.textContent));

                    const newParticipantRemoveEls = document.querySelectorAll('.js-participant-remove');
                    const newExpenseRemoveEls = document.querySelectorAll('.js-expense-remove');
                    newExpenseRemoveEls.forEach(element => expenseRemoveHandler(element));
                    newParticipantRemoveEls.forEach(element => participantRemoveHandler(element))
                }
            )
        });
    };

    ajaxForms.forEach(form => joinRequestFormHandler(form));

});



