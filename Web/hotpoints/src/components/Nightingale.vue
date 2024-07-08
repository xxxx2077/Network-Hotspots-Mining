<template>
    <div ref="nightingale" style="width: 100%; height: 100%;"></div>
</template>

<script>
import * as echarts from 'echarts';

export default {
    name: 'Nightingale',
    props: {
        titleText: { type: String, default: '' },
        valueData: { type: Array, required: true },
        fontColor: { type: String, default: 'black' }
    },
    data() {
        return {
            chartInstance: null,
        }
    },
    mounted() {
        this.initChart();
        this.updateChart();
        window.addEventListener("resize", () => {
            this.chartInstance.resize();
        })
    },
    destroyed() {
        this.chartInstance.dispose();
        window.removeEventListener("resize", this.chartInstance);
    },
    methods: {
        initChart() {
            this.chartInstance = echarts.init(this.$refs['nightingale']);
        },
        updateChart() {
            const len = this.$props.valueData.length;
            const blankChart = [];
            for (var i = 0; i < len; i++) {
                blankChart.push({ value: 0, itemStyle: { normal: { color: "rgba(0,0,0,0)" } } });
            }
            var newData = this.$props.valueData.concat(blankChart);

            const option = {
                tooltip: {
                    trigger: 'item',
                    axisPointer: {
                        type: 'shadow'
                    },
                    backgroundColor: 'rgba(104, 104, 104, 0.7)', // 悬浮框背景色
                    borderColor: '#000', // 悬浮框边框颜色
                    borderWidth: 1, // 悬浮框边框宽度
                    textStyle: { // 悬浮框文字样式
                        color: 'white',
                        fontSize: 12
                    }
                },
                title: {
                    text: this.$props.titleText,
                    textStyle: {
                        color: this.$props.fontColor,
                    },
                    left: '3%',
                    top: '3%',
                },
                legend: {
                    type: 'scroll',
                    top: '3%',
                    left: '40%',
                    icon: 'circle',
                    textStyle: {
                        color: this.$props.fontColor
                    }
                },
                label: {
                    show: false,
                    color: this.$props.fontColor
                },
                labelLine: {
                    show: false
                },
                series: [
                    {
                        name: this.$props.titleText,
                        type: 'pie',
                        radius: ['10%', '80%'],
                        center: ['50%', '38%'],
                        // 设置角度
                        startAngle: 0,
                        roseType: 'area',
                        data: newData
                    }
                ]
            }
            this.chartInstance.setOption(option);
        }
    },
    watch: {
        valueData(newVal) {
            this.chartInstance.setOption(option);
        }
    }
}
</script>