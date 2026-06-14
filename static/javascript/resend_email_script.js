const resendRemainingEl = document.getElementById('resend-remaining');
const resendCountdownTextEl = document.getElementById('resend-countdown-text');
const resendTimerEl = document.getElementById('resend-timer');
const resendBtnEl = document.getElementById('resend-btn');

let resendRemainTime = Number(resendRemainingEl.value) + 1;
if (resendRemainTime <= 0) {
    resendRemainTime = 0
} else{
    resendBtnEl.classList.add('hidden')
}

const calculateResendTex = function (time) {
    if (time <= 0) {
        return '0 seconds'
    }
    if (time <= 60) {
        return String(time) + ' seconds'
    }
    const minutes = parseInt(time / 60, 10);
    const seconds = Math.round(((time / 60) - minutes) * 60);
    const strMin = String(minutes);
    let strSec = String(seconds);
    if (seconds < 10) {
        strSec = '0' + strSec;
    }
    return strMin + ':' + strSec
}


const timer = setInterval(function () {
    resendRemainTime -= 1;
    resendRemainingEl.value = resendRemainTime;
    if (resendRemainTime <= 0) {
        clearInterval(timer);
        resendTimerEl.classList.add('hidden');
        resendBtnEl.classList.remove('hidden');
    } else {
        resendCountdownTextEl.innerText = calculateResendTex(resendRemainTime);
        resendTimerEl.classList.remove('hidden');
    }
}, 1000);

