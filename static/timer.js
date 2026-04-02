const TIMER_KEY = 'timerEndTime';
const DURATION_MS = 120 * 60 * 1000;

function startTimer() {
    let endTime = sessionStorage.getItem(TIMER_KEY);

    if (!endTime) {
        endTime = new Date().getTime() + DURATION_MS;
        sessionStorage.setItem(TIMER_KEY, endTime);
    } else {
        endTime = Number(endTime);
    }

    const interval = setInterval(function () {
        const now = new Date().getTime();
        const remainingTime = endTime - now;
        const display = document.getElementById('timer-display');

        if (remainingTime >= 0) {
            const hour =  Math.floor((remainingTime % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((remainingTime % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((remainingTime % (1000 * 60)) / 1000);

            if (display) {
                display.textContent = `${hour <10 ? '0' + hour : hour}h ${minutes < 10 ? '0' + minutes : minutes}m ${seconds < 10 ? '0' + seconds : seconds}s`;
            }
        } else {
            clearInterval(interval);
            if (display) {
                display.textContent = "EXPIRED";
                fetch('/no_more_times', {})
            }
            sessionStorage.removeItem(TIMER_KEY);
        }
    }, 1000);
}

startTimer();