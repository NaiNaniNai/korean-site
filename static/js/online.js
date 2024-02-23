document.addEventListener("DOMContentLoaded", function() {

    const elem = document.getElementById('self_rating_month_data')
    if (!elem) {}
    else {
        const monthOnlineData = JSON.parse(elem.textContent);
        const monthMinutesData = Object.values(monthOnlineData).map(value => Math.max(Math.ceil(value / 60), 1));

        const today = new Date()
        const monthStartDate = new Date(today.getFullYear(), today.getMonth(), 1)
        const monthEndDate = today
        const monthNumberOfDays = Math.ceil((monthEndDate - monthStartDate) / (1000 * 60 * 60 * 24));

        const formattedMonthOnlineData = Object.keys(monthOnlineData).reduce((acc, date) => {
        const formattedDate = `${today.getFullYear()}-${(today.getMonth() + 1).toString().padStart(2, '0')}-${date.padStart(2, '0')}`;
        acc[formattedDate] = monthOnlineData[date];
        return acc;
        }, {}
        );

        const monthDateArray = Array.from({length: monthNumberOfDays}, (_, index) => {
            const date = new Date(monthStartDate);
            date.setDate(monthStartDate.getDate() + index + 1);
            return date.toISOString().split('T')[0];
        });

        const monthResultData = monthDateArray.reduce((acc, currentDate) => {
            const seconds = formattedMonthOnlineData[currentDate] || 0;
            const minutes = Math.ceil(seconds / 60);
            acc[currentDate] = minutes;
            return acc;
        }, {});

        const monthCtx = document.getElementById('month_online').getContext('2d');
        const monthChart = new Chart(monthCtx, {
            type: 'bar',
            data: {
                labels: Object.keys(monthResultData),
                datasets: [{
                    label: 'Время онлайн в минутах за месяц',
                    data: Object.values(monthResultData),
                    backgroundColor: 'rgba(169, 209, 142, 0.6)',
                    borderColor: 'rgba(169, 209, 142, 1)',
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

        const weekOnlineData = JSON.parse(document.getElementById('self_rating_week_data').textContent);
        const weekMinutesData = Object.values(weekOnlineData).map(value => Math.max(Math.ceil(value / 60), 1));


        const getLastDayOfWeek = (date) => {
            const lastDayOfWeek = new Date(date);
            const diff = date.getDate() + (7 - date.getDay());
            lastDayOfWeek.setDate(diff);
            lastDayOfWeek.setHours(0, 0, 0, 0);
            return lastDayOfWeek;
        };

        const getFirstDayOfWeek = (date) => {
            const dayOfWeek = date.getDay();
            const firstDayOfWeek = new Date(date);
            const diff = date.getDate() - dayOfWeek + (dayOfWeek === 0 ? -6 : 1);
            firstDayOfWeek.setDate(diff);
            firstDayOfWeek.setHours(0, 0, 0, 0);
            return firstDayOfWeek;
        };

        const weekStartDate = getFirstDayOfWeek(today);
        const weekEndDate = getLastDayOfWeek(today);
        const getDaysDifference = (date1, date2) => {
            const oneDay = 1000 * 60 * 60 * 24;
            const diffInMs = Math.abs(date2 - date1);
            return Math.round(diffInMs / oneDay);
        };


        const weekNumberOfDays = getDaysDifference(weekStartDate, weekEndDate) + 1;

        const formattedWeekOnlineData = Object.keys(weekOnlineData).reduce((acc, date) => {
        const today = new Date();
        const formattedDate = `${today.getFullYear()}-${(today.getMonth() + 1).toString().padStart(2, '0')}-${date.padStart(2, '0')}`;
        acc[formattedDate] = weekOnlineData[date];
        return acc;
        }, {}
        );

        const weekDateArray = Array.from({length: weekNumberOfDays}, (_, index) => {
            const date = new Date(weekStartDate);
            date.setDate(weekStartDate.getDate() + index + 1);
            return date.toISOString().split('T')[0];
        });

        const weekResultData = weekDateArray.reduce((acc, currentDate) => {
            const seconds = formattedMonthOnlineData[currentDate] || 0;
            const minutes = Math.ceil(seconds / 60);
            acc[currentDate] = minutes;
            return acc;
        }, {});


        const getDayOfWeek = (date) => {
        const options = { weekday: 'short' };
        return date.toLocaleDateString('ru-ru', options);
        };

        const labels = Object.keys(weekResultData).map(date => {
            const currentDate = new Date(date);
            return getDayOfWeek(currentDate);
        });

        const weekCtx = document.getElementById('week_online').getContext('2d');
        const weekChart = new Chart(weekCtx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Время онлайн в минутах за неделю',
                    data: Object.values(weekResultData),
                    backgroundColor: 'rgba(169, 209, 142, 0.6)',
                    borderColor: 'rgba(169, 209, 142, 1)',
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
    }
});
