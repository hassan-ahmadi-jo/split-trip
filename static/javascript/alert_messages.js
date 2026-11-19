export const showSuccessAlert = (english_message = null, persian_message = null) => {
    const language = window.location.pathname.split('/')[1];

    let message = english_message
    let error_position = 'top-start'
    if (language === 'fa') {
        message = persian_message;
        error_position = 'top-end'
    }
    
    
    if (!message) {
        message = 'Request completed successfully'
        if(language === 'fa') {
            message = 'درخواست با موفقیت انجام شد'
        } 
    }

    Swal.fire({
        toast: true,
        position: error_position,
        icon: 'success',
        title: message,
        showConfirmButton: false,
        timer: 2000,
        timerProgressBar: true,
    });
}

export const showErrorAlert = (english_message = null, persian_message = null) => {
    const language = window.location.pathname.split('/')[1];

    let message = english_message
    let error_position = 'top-start'
    if (language === 'fa') {
        message = persian_message;
        error_position = 'top-end'
    }
    
    
    if (!message) {
        message = 'Error processing request'
        if(language === 'fa') {
            message = 'خطا در انجام درخواست'
        } 
    }

    Swal.fire({
        toast: true,
        position: error_position,
        icon: 'error',
        title: message,
        showConfirmButton: false,
        timer: 2000,
        timerProgressBar: true,
    });
}