const TIMER_KEY = 'timerEndTime';
const DURATION_MS = 30 * 60 * 1000;

function startPersistentTimer() {
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
            const minutes = Math.floor((remainingTime % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((remainingTime % (1000 * 60)) / 1000);

            if (display) {
                display.textContent = `${minutes < 10 ? '0' + minutes : minutes}m ${seconds < 10 ? '0' + seconds : seconds}s`;
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

startPersistentTimer();