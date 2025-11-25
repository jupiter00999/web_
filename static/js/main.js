// static/js/main.js
document.addEventListener('DOMContentLoaded', function() {
    const startBtn = document.getElementById('start-btn');
    const stopBtn = document.getElementById('stop-btn');
    const avatarImg = document.getElementById('avatar-img');
    const nameDisplay = document.getElementById('name-display');

    let lotteryInterval;

    // 随机点名
    startBtn.addEventListener('click', () => {
        if (lotteryInterval) return; // 防止重复点击

        startBtn.disabled = true;
        stopBtn.disabled = false;

        lotteryInterval = setInterval(() => {
            const randomIndex = Math.floor(Math.random() * users.length);
            const randomUser = users[randomIndex];
            avatarImg.src = randomUser.img;
            nameDisplay.textContent = randomUser.name;
        }, 50); // 每50毫秒切换一次
    });

    stopBtn.addEventListener('click', () => {
        if (!lotteryInterval) return;

        clearInterval(lotteryInterval);
        lotteryInterval = null;

        startBtn.disabled = false;
        stopBtn.disabled = true;
        // 可以在这里添加中奖后的特效或提示
        alert(`恭喜 ${nameDisplay.textContent} 中奖！`);
    });

    // --- ECharts 数据可视化 ---
    async function initCharts() {
        const response = await fetch('/api/charts_data');
        const data = await response.json();

        // 1. 销量折线图
        const salesChart = echarts.init(document.getElementById('sales-chart'));
        salesChart.setOption({
            title: { text: '近30天销量趋势' },
            tooltip: { trigger: 'axis' },
            xAxis: { type: 'category', data: data.sales.dates },
            yAxis: { type: 'value' },
            series: [{ name: '销量', data: data.sales.amounts, type: 'line', smooth: true }]
        });

        // 2. 年龄分布饼图
        const ageChart = echarts.init(document.getElementById('age-chart'));
        ageChart.setOption({
            title: { text: '用户年龄分布' },
            tooltip: { trigger: 'item' },
            series: [{
                type: 'pie',
                radius: '50%',
                data: data.age.groups.map((group, i) => ({ value: data.age.counts[i], name: group }))
            }]
        });

        // 3. 页面浏览量柱状图
        const viewChart = echarts.init(document.getElementById('view-chart'));
        viewChart.setOption({
            title: { text: '各页面浏览量' },
            tooltip: { trigger: 'axis' },
            xAxis: { type: 'category', data: data.view.pages },
            yAxis: { type: 'value' },
            series: [{ name: '浏览量', data: data.view.view_counts, type: 'bar' }]
        });

        // 4. 分类关注数柱状图
        const followChart = echarts.init(document.getElementById('follow-chart'));
        followChart.setOption({
            title: { text: '各分类关注数' },
            tooltip: { trigger: 'axis' },
            xAxis: { type: 'category', data: data.follow.categories },
            yAxis: { type: 'value' },
            series: [{ name: '关注数', data: data.follow.follower_counts, type: 'bar' }]
        });
    }

    initCharts();
});
