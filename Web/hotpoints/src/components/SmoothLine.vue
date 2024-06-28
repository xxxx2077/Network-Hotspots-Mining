<template>
    <div ref="SmoothLine" style="width: 100%; height: 100%;"></div>
</template>

<script>
import * as echarts from 'echarts';

export default {
    name: 'SmoothLine',
    props: {
        titleText: { type: String, default: '' },
        xData: { type: Array, required: true },
        valueData: { type: Array, required: true },
        fontColor: { type: String, default: 'black' }
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
                color: ['#05fbff'],
                title: {
                    text: this.$props.titleText,
                    textStyle: {
                        color: this.$props.fontColor,
                    },
                    left: '3%',
                    top: '3%',
                },
                grid: {
                    bottom: '15%',
                },
                xAxis: {
                    data: this.$props.xData,
                    axisLabel: {
                        textStyle: {
                            color: this.$props.fontColor
                        }
                    },
                    axisLine: {
                        lineStyle: {
                            color: this.$props.fontColor
                        }
                    }
                },
                yAxis: {
                    axisLabel: {
                        textStyle: {
                            color: this.$props.fontColor
                        }
                    }
                },
                series: [{
                    data: this.$props.valueData,
                    type: 'line',
                    smooth: true,
                    areaStyle: {
                        color: 'rgba(5, 251, 255, 0.6)'
                    },
                }]
            },
        }
    },
    mounted() {
        this.initChart();
        this.updateChart();
    },
    methods: {
        initChart() {
            this.chartInstance = echarts.init(this.$refs['SmoothLine']);
        },
        updateChart() {
            this.chartInstance.setOption(this.option);
        }
    }
}
</script>