<template>
    <div ref="ring" style="width: 100%; height: 100%;"></div>
</template>

<script>
import * as echarts from 'echarts';

export default {
    name: 'Ring',
    props: {
        titleText: { type: String, default: '' },
        valueData: { type: Array, required: true },
        color: { type: Array, default: [] },
        flag: { type: Boolean, required: true }
    },
    data() {
        return {
            chartInstance: null,
            option: {
                title: {
                    text: this.$props.titleText,
                    textStyle: {
                        color: 'white',
                    },
                    left: '3%',
                    top: '3%',
                },
                // legend: {
                //     top: '3%',
                //     left: '35%',
                //     icon: 'circle',
                //     textStyle: {
                //         color: 'white'
                //     }
                // },
                series: [
                    {
                        type: 'pie',
                        radius: ['50%', '70%'],
                        center: ['50%', '50%'],
                        avoidLabelOverlap: false,
                        label: {
                            show: false,
                            position: 'center'
                        },
                        labelLine: {
                            show: false
                        },
                        emphasis: {
                            label: {
                                show: true,
                                fontSize: '30',
                                formatter: '{b}\n{c}',
                            }
                        },
                        data: this.$props.valueData
                    }
                ]
            }
        }
    },
    mounted() {
        this.initChart();
        this.updateChart();
        // 窗口大小改变更新图表
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
            this.chartInstance = echarts.init(this.$refs['ring']);
        },
        updateChart() {
            if (this.$props.color.length !== 0) {
                for (var i = 0; i < this.$props.valueData.length; i++) {
                    var data = this.option.series[0].data.shift();
                    this.$set(data, 'itemStyle', { color: this.$props.color[i] });
                    this.option.series[0].data.push(data);
                }
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