<template>
    <div ref="basicBar" style="width: 100%; height: 100%;"></div>
</template>

<script>
import * as echarts from 'echarts'

export default {
    name: 'BasicBar',
    props: {
        titleText: { type: String, required: true },
        xData: { type: Array, required: true },
        barNum: { type: Number, required: true },
        barName: { type: Array, required: true },
        barData: { type: Array, required: true },
        flag: { type: Boolean, required: true },
    },
    data() {
        return {
            chartInstance: null,
            option: {
                tooltip: {
                    trigger: 'axis',
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
                color: ['#ff2b05', '#ff6905', '#05b4ff', '#05fbff', '#dcffff'],
                title: {
                    text: this.$props.titleText,
                    textStyle: {
                        color: 'white',
                    },
                    left: '3%',
                    top: '3%',
                },
                legend: {
                    right: '3%',
                    top: '10%',
                    icon: 'roundRect',
                    textStyle: {
                        color: 'white'
                    }
                },
                grid: {
                    bottom: '15%',
                },
                xAxis: {
                    data: this.$props.xData,
                    axisLabel: {
                        textStyle: {
                            color: 'white'
                        }
                    },
                    axisLine: {
                        lineStyle: {
                            color: 'white'
                        }
                    }
                },
                yAxis: {
                    axisLabel: {
                        textStyle: {
                            color: 'white'
                        }
                    }
                },
                series: []
            },
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
            this.chartInstance = echarts.init(this.$refs['basicBar']);
        },
        updateChart() {
            this.option.series = [];
            for (var i = 0; i < this.$props.barNum; i++) {
                var obj = {
                    name: this.$props.barName[i],
                    data: this.$props.barData[i],
                    type: 'bar'
                }
                this.option.series.push(obj);
            }
            this.chartInstance.setOption(this.option);
        }
    },
    watch: {
        flag(newVal) {
            this.updateChart();
        }
    }
}
</script>