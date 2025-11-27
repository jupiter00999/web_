document.addEventListener('DOMContentLoaded', function() {
    // 初始化销量图表
    initSalesChart();
});

function initSalesChart() {
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.getElementById('sales-chart'));

    // 加载销量数据
    fetch('/api/sales-data')
        .then(response => response.json())
        .then(data => {
            // 准备图表数据
            var productNames = data.map(item => item.name);
            var salesData = data.map(item => item.sales);
            var priceData = data.map(item => '￥' + item.price);

            // 指定图表的配置项和数据
            var option = {
                title: {
                    text: '商品销量统计',
                    left: 'center',
                    textStyle: {
                        color: '#333'
                    }
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'shadow'
                    },
                    formatter: function(params) {
                        var data = params[0];
                        return data.name + '<br/>' +
                               '销量: ' + data.value + ' 件<br/>' +
                               '价格: ' + priceData[data.dataIndex];
                    }
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '15%',
                    containLabel: true
                },
                xAxis: {
                    type: 'category',
                    data: productNames,
                    axisLabel: {
                        interval: 0,
                        rotate: 45,
                        fontSize: 10
                    }
                },
                yAxis: {
                    type: 'value',
                    name: '销量(件)',
                    axisLabel: {
                        formatter: '{value}'
                    }
                },
                series: [{
                    name: '销量',
                    type: 'bar',
                    data: salesData,
                    itemStyle: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                            {offset: 0, color: '#83bff6'},
                            {offset: 0.5, color: '#188df0'},
                            {offset: 1, color: '#188df0'}
                        ])
                    },
                    emphasis: {
                        itemStyle: {
                            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                                {offset: 0, color: '#2378f7'},
                                {offset: 0.7, color: '#2378f7'},
                                {offset: 1, color: '#83bff6'}
                            ])
                        }
                    },
                    label: {
                        show: true,
                        position: 'top',
                        formatter: '{c}'
                    }
                }]
            };

            // 使用刚指定的配置项和数据显示图表
            myChart.setOption(option);

            // 响应式调整
            window.addEventListener('resize', function() {
                myChart.resize();
            });
        })
        .catch(error => {
            console.error('加载销量数据失败:', error);
            document.getElementById('sales-chart').innerHTML =
                '<div style="text-align: center; padding: 50px; color: #666;">销量数据加载失败</div>';
        });
}
