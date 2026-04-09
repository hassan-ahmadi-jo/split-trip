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
                }
            )
        });
    };

    ajaxForms.forEach(form => joinRequestFormHandler(form));

});



