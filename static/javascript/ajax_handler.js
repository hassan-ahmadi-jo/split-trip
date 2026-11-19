import { showErrorAlert } from "./alert_messages.js";
// AJAX
const ajaxContainerEls = document.querySelectorAll('.js-ajax-container');

ajaxContainerEls.forEach(function (container) {
    container.addEventListener('submit', async function (event) {
        const form = event.target.closest('.js-ajax-form');
        
        if (!form || !container.contains(form)) return;

        event.preventDefault();

        const formData = new FormData(form);
        
        if (event.submitter && event.submitter.name) {
            formData.append(event.submitter.name, event.submitter.value);
        }

        const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
        if (!csrfInput) {
            console.error('CSRF token not found!');
            return;
        }
        
        const csrfToken = csrfInput.value;
        const url = form.action;

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: { "X-CSRFToken": csrfToken },
                body: formData
            });
            
            if (!response.ok) {
                throw new Error('HTTP error ' + response.status);
            }

            const htmlData = await response.text();
            
            if (htmlData) {
                container.innerHTML = htmlData;

            }
        } catch (error) {
            console.error('AJAX submission failed:', error);
            showErrorAlert();
        }
    });
});

