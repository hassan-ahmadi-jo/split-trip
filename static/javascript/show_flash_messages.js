import { showSuccessAlert, showErrorAlert } from "./alert_messages.js";
const flashMessageEls = document.querySelectorAll('.js-flash-message');

if (flashMessageEls.length > 0){
    flashMessageEls.forEach((element) => {
        if (element.dataset.alertType === 'success') {
            showSuccessAlert();
        } else {
            showErrorAlert();
        }
    })
}
