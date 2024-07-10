<template>
    <el-container>
        <el-aside width="15%">
            <div style="padding-top: 3%;">
                <span class="title">中大热点系统</span>
            </div>
            <el-menu class="menu" :router="true" :default-active="$route.path">
                <el-menu-item v-for="(item, index_) in menuItem" :key="index_" :index="item.path">
                    <span class="section">{{ item.section }}</span>
                </el-menu-item>
            </el-menu>
        </el-aside>
        <el-main>
            <router-view></router-view>
        </el-main>
    </el-container>
</template>

<script>
export default {
    name: 'Menu',
    data() {
        return {
            menuItem: [{
                section: '首页',
                path: '/'
            }, {
                section: '话题详情',
                path: '/menu/topic/:id'
            },]
        }
    },
    methods: {

    }
}
</script>

<style>
.el-container {
    padding: 0px;
    margin: 0px;
    height: 100%;
}

.el-aside {
    background-color: #20222A;
    /* display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center; */
    height: 100vh;
}

.title {
    color: white;
    font-size: larger;
    font-weight: bold;
}

.menu {
    text-align: center;
    background-color: #20222A;
}

.el-menu-item {
    color: white;
}

.el-menu-item.is-active {
    color: white;
    background-color: #8080FF;
}

.section {
    color: white;
    font-size: large;
    font-weight: bold;
}

.el-main {
    padding-top: 10px;
}
</style>