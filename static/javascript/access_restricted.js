// Access Restricted
const can_edit_event_info = JSON.parse(
    document.getElementById('can_edit_event_info').textContent
);

const accessRestrictedHandler = function (el) {
    el.disabled = true;
    el.removeAttribute("href");
    el.classList.add('access-restricted');
    el.title = 'Members cannot access this section.';
};

if (!can_edit_event_info) {
    restrictedEls = document.querySelectorAll('.js-access-restricted');
    restrictedEls.forEach(element => {accessRestrictedHandler(element)});
};


