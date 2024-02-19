document.addEventListener("DOMContentLoaded", function() {

    const daysOnlineData = JSON.parse(document.getElementById('self_rating_data').textContent);
    const minutesData = Object.values(daysOnlineData).map(value => Math.max(Math.ceil(value / 60), 1));

    const today = new Date()
    const startDate = new Date(today.getFullYear(), today.getMonth(), 1)
    const endDate = today
    const numberOfDays = Math.ceil((endDate - startDate) / (1000 * 60 * 60 * 24));

    const formattedDaysOnlineData = Object.keys(daysOnlineData).reduce((acc, date) => {
    const today = new Date();
    const formattedDate = `${today.getFullYear()}-${(today.getMonth() + 1).toString().padStart(2, '0')}-${date.padStart(2, '0')}`;
    acc[formattedDate] = daysOnlineData[date];
    return acc;
    }, {}
    );

    const dateArray = Array.from({length: numberOfDays}, (_, index) => {
        const date = new Date(startDate);
        date.setDate(startDate.getDate() + index + 1);
        return date.toISOString().split('T')[0];
    });

    const resultData = dateArray.reduce((acc, currentDate) => {
        const seconds = formattedDaysOnlineData[currentDate] || 0; // Если данных нет, используем 0
        const minutes = Math.ceil(seconds / 60); // Переводим секунды в минуты и округляем до целого в большую сторону
        acc[currentDate] = minutes;
        return acc;
    }, {});

    const ctx = document.getElementById('onlineChart').getContext('2d');
    const chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(resultData),
            datasets: [{
                label: 'Время онлайн в минутах',
                data: Object.values(resultData),
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    type: 'logarithmic',
                    min: 0.1,
                    ticks: {
                        callback: function(value, index, values) {
                            return Number(value.toString());
                        },
                        maxTicksLimit: 6
                    }
                }
            }
        }
    });
});
