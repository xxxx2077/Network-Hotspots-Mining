<template>
    <div ref="stackedBar" style="width: 100%; height: 100%;"></div>
</template>

<script>
import * as echarts from 'echarts';

export default {
    name: 'StackedBar',
    props: {
        titleText: { type: String, required: true },
        xData: { type: Array, required: true },
        userData: { type: Array, required: true },
        selfMediaData: { type: Array, required: true },
        mainMediaData: { type: Array, required: true },
    },
    data() {
        return {
            chartInstance: null,
            stackedBarOption: {
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
                title: {
                    text: this.$props.titleText,
                    textStyle: {
                        color: 'white',
                    },
                    left: '3%',
                    top: '3%',
                },
                legend: {
                    data: [{
                        name: '个人用户',
                        icon: 'roundRect',
                        textStyle: {
                            color: 'white'
                        }
                    }, {
                        name: '自媒体',
                        icon: 'roundRect',
                        textStyle: {
                            color: 'white'
                        }
                    }, {
                        name: '主流媒体',
                        icon: 'roundRect',
                        textStyle: {
                            color: 'white'
                        }
                    }],
                    right: '3%',
                    top: '3%'
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
                series: [
                    {
                        name: '个人用户',
                        data: this.$props.userData,
                        type: 'bar',
                        stack: 'x',
                        itemStyle: {
                            normal: {
                                color: '#dcffff'
                            }
                        },
                    },
                    {
                        name: '自媒体',
                        data: this.$props.selfMediaData,
                        type: 'bar',
                        stack: 'x',
                        itemStyle: {
                            normal: {
                                color: '#05fbff'
                            }
                        },
                    },
                    {
                        name: '主流媒体',
                        data: this.$props.mainMediaData,
                        type: 'bar',
                        stack: 'x',
                        itemStyle: {
                            normal: {
                                color: '#05b4ff'
                            }
                        },
                    }
                ]
            },
        };
    },
    mounted() {
        this.initChart();
        this.updateChart();
    },
    methods: {
        initChart() {
            this.chartInstance = echarts.init(this.$refs['stackedBar']);
        },
        updateChart() {
            this.chartInstance.setOption(this.stackedBarOption);
        }
    }
}
</script>