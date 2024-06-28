<template>
    <dv-scroll-board :config="config" style="width: 100%; height: 100%" @click="onClick" />
</template>

<script>
export default {
    name: 'Carousel',
    props: {
        header: { type: Array, requried: true },
        headerBGC: { type: String, default: '#131e4d' },
        data: { type: Array, requried: true },
        rowNum: { type: Number, default: 5 },
        columnWidth: { type: Array, default: [] },
        onClick: { type: Function, default: null },
    },
    data() {
        return {
            config: {
                header: this.$props.header,
                data: this.$props.data,
                rowNum: this.$props.rowNum,
                headerBGC: this.$props.headerBGC,
                columnWidth: this.$props.columnWidth,
                align: 'center',
                index: true,
            }
        }
    },
}
</script>