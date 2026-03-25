const priceEls = document.querySelectorAll('.js-price')

const formatPrice = function (price) {
    let number = String(price).replace(/[^\d.]/g, '').replace(/(\..*)\./g, '$1');
    if (parseFloat("number") == 0 || number === "") {
        return '0'
    };
    dot_index = number.indexOf('.');
    let integer_part = '';
    let decimal_part = '';

    if (dot_index == -1) {
        integer_part = number;
    } else {
        integer_part = number.slice(0, dot_index);
        decimal_part = number.slice(dot_index + 1);
    }
    decimal_part = decimal_part.slice(0, 2)
    if (parseFloat(decimal_part) == 0){
        decimal_part = '';
        dot_index = -1;
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

// priceEls.forEach(element => element.value = formatPrice(element.value));
priceEls.forEach(element => element.textContent = formatPrice(element.textContent));

