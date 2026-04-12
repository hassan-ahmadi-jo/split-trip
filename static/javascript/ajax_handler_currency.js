// AJAX
const ajaxContainerEl = document.querySelector('.js-ajax-container');
const ajaxFormEl = document.querySelector('.js-ajax-form');
currencyUnitEls = document.querySelectorAll('.js-currency-unit')

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
            response => response.json()
        ).then(
            data => {
                ajaxContainerEl.innerHTML = data.html_data;           

                const newajaxForm = document.querySelector('.js-ajax-form');
                joinRequestFormHandler(newajaxForm);
                
                currencyUnitEls.forEach(element => {
                    element.textContent = data.active_currency
                });
            }
        )
    });
};

joinRequestFormHandler(ajaxFormEl);




