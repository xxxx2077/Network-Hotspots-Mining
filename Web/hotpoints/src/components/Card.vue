<template>
    <el-card shadow="always" style="width: 100%; height: 100%;">
        <template #header>
            <div style="widows: 100%; height: 100%; display: flex; align-items: center;">
                <div style="width: 8px; height: 100%; background-color: #8080FF;"></div>
                <span style="font-weight: bold; margin-left: 5px;">{{ title }}</span>
            </div>
        </template>
        <slot></slot>
    </el-card>
</template>

<script>
export default {
    name: 'Card',
    props: {
        title: { type: String, require: true },
    },
    data() {
        return {

        }
    },
    methods: {

    }
}
</script>

<style>
.el-card__header {
    width: 100%;
    height: 15%;
    padding: 5px 20px;
}

.el-card__body {
    width: 100%;
    height: 85%;
    padding: 0px;
}
</style>