<template>
    <div style="width: 100%; height: 100%;">
        <div style="width: 100%; height: 30%;">
            <Card title="话题概况">
                <div style="display: flex; width: 100%; height: 100%;">
                    <div style="width: 45%; height: 100%; display: flex; flex-direction: column; text-align: left;">
                        <span style="float: left; margin-left: 3%; margin-top: 2%;">标题：{{ topic.topic }}</span>
                        <div style="width: 100%; margin-left: 3%; margin-top: 2%; display: flex; text-align: start;">
                            <span style="">简介：</span>
                            <el-input v-model="topic.content" type="textarea" :rows="5" style="width: 85%;"
                                :readonly="true"></el-input>
                        </div>
                    </div>
                    <div style="width: 48%; height: 100%; margin-left: auto; display: flex; align-items: center;">
                        <div class="dataCard"
                            style="background: linear-gradient(to right, #FBC2EB, #A28CD1); margin-left: 2%;">
                            <span class="detail" style="margin-top: 20%;">实时热度</span>
                            <span class="detail" style="margin-top: auto; margin-bottom: 20%;">{{ topic.hotValue }}</span>
                            <!-- <span class="detail" style="margin-top: auto; margin-bottom: 10%;">较昨日上升10%</span> -->
                        </div>
                        <div class="dataCard"
                            style="background: linear-gradient(to right, #F2869F, #FCC687); margin-left: auto;">
                            <span class="detail" style="margin-top: 20%;">风险预警</span>
                            <span class="detail" style="margin-top: auto; margin-bottom: 20%;">{{ topic.warnValue }}</span>
                            <!-- <span class="detail" style="margin-top: auto; margin-bottom: 10%;">较昨日上升0%</span> -->
                        </div>
                        <div class="dataCard"
                            style="background: linear-gradient(to right, #08BAFC, rgba(5, 251, 255, 0.6)); margin-left: auto; margin-right: 2%;">
                            <span class="detail" style="margin-top: 20%;">今日访问量</span>
                            <span class="detail" style="margin-top: auto; margin-bottom: 20%;">{{ topic.visits }}</span>
                            <!-- <span class="detail" style="margin-top: auto; margin-bottom: 10%;">较昨日上升10%</span> -->
                        </div>
                    </div>
                </div>
            </Card>
        </div>
        <el-row style="height: 29%; margin-top: 1%;" :gutter="15">
            <el-col :span="6" style="height: 100%;">
                <Card title="舆论情感分析">
                    <div style="width: 100%; height: 100%; display: flex;">
                        <Ring :valueData="ringData" :color="['#009DFF', '#22E4FF', '#4985F0', '#04E38A']"></Ring>
                    </div>
                </Card>
            </el-col>
            <el-col :span="6" style="height: 100%;">
                <Card title="平台影响占比">
                    <Nightingale :valueData="nightinggaleData"></Nightingale>
                </Card>
            </el-col>
            <el-col :span="12" style="height: 100%;">
                <Card title="访问量趋势">
                    <SmoothLine :xData="visitTrendX" :valueData="visitTrendData"></SmoothLine>
                </Card>
            </el-col>
        </el-row>
        <el-row style="height: 39%; margin-top: 1%;" :gutter="15">
            <el-col :span="12" style="height: 100%;">
                <Card title="事件图谱">
                    <Relation></Relation>
                </Card>
            </el-col>
            <el-col :span="12" style="height: 100%;">
                <Card title="话题内事件榜">
                    <Carousel :header="['类型', '平台', '帖子', '热度']" headerBGC="#0669AF" :data="postList" :rowNum="5"
                        :columnWidth="[50, 90, 90, 250, 90]" :flag="postListFlag" :onClick="clickCarousel"></Carousel>
                </Card>
            </el-col>
        </el-row>
    </div>
</template>

<script>
import Card from '@/components/Card.vue';
import Ring from '@/components/Ring.vue';
import Nightingale from '@/components/Nightingale.vue';
import SmoothLine from '@/components/SmoothLine.vue';
import Carousel from '@/components/Carousel.vue';
import Relation from '@/components/Relation.vue';
import { getTopicDetail, getTopicVisits, getPostList } from '@/api/topic';

export default {
    name: 'Topic',
    components: {
        Card,
        Ring,
        Nightingale,
        SmoothLine,
        Carousel,
        Relation,
    },
    data() {
        return {
            topicID: 0,
            topic: {
                title: '',
                content: '',
                hotVal: 0,
                warnVal: 0,
                visits: 0,
            },
            ringData: [
                { name: '一类', value: 20 },
                { name: '二类', value: 16 },
                { name: '三类', value: 5 },
                { name: '四类', value: 9 },
            ],
            nightinggaleData: [
                { name: '集市', value: 40 },
                { name: '小红书', value: 30 },
                { name: '抖音', value: 30 },
            ],
            visitTrendX: [],
            visitTrendData: [],
            postList: [['', '', '', '']],
            postListFlag: false,
        }
    },
    created() {
        this.topicID = this.$route.params.id;
    },
    mounted() {
        // 获取话题详情
        getTopicDetail(this.topicID).then((res) => {
            if (res.status == 200) {
                this.topic = res.data;
            }
        }).catch((err) => {
            console.log(err);
        })

        // 获取话题浏览量
        getTopicVisits(this.topicID).then((res) => {
            if (res.status == 200) {
                res.data.data.forEach(obj => {
                    this.visitTrendX.push(obj.date);
                    this.visitTrendData.push(obj.visit);
                })
            }
        }).catch((err) => {
            console.log(err);
        })

        // 获取话题内帖子
        getPostList(this.topicID).then((res) => {
            if (res.status == 200) {
                this.postList.pop();
                for (let obj of res.data.data) {
                    const arr = Object.keys(obj).map(item => obj[item]);
                    this.postList.push(arr);
                }
                this.postListFlag = !this.postListFlag;
            }
        }).catch((err) => {
            console.log(err);
        })
    },
    methods: {
        clickCarousel(config) {
            console.log('开发中...');
        }
    }
}
</script>

<style scoped>
.dataCard {
    width: 30%;
    height: 80%;
    border-radius: 15px;
    display: flex;
    flex-direction: column;
}

.detail {
    color: white;
    font-size: large;
    font-weight: bold;
}
</style>