<template>
  <dv-full-screen-container>
    <!-- <div id="dv-full-screen-container" style="width: 100%; height: 100%;"> -->
    <el-row justify="center">
      <el-col :span="10"><dv-decoration-8 style="height: 60px;" /></el-col>
      <el-col :span="4" style="margin-top: 10px;"><span class="title">中大热度数据面板</span></el-col>
      <el-col :span="10"><dv-decoration-8 :reverse="true" style="height: 60px;" /></el-col>
    </el-row>
    <el-row style="height: 50%;">
      <el-col :span="7" style="height: 100%;">
        <dv-border-box-12 style="height: 50%;">
          <StackedBar titleText="数据类型统计" :xData="stackedBarXData" :userData="stackedBarUserData"
            :selfMediaData="stackedBarSelfData" :mainMediaData="stackedBarMainData"></StackedBar>
        </dv-border-box-12>
        <dv-border-box-12 style="height: 50%;">
          <Nightingale titleText="热点数据分布" :valueData="nightinggaleData" fontColor="white"></Nightingale>
        </dv-border-box-12>
      </el-col>
      <el-col :span="10" style="height: 100%;">
        <dv-border-box-12 style="height: 65%;">
          <BasicBar titleText="本周热度数据统计" :barNum="4" :barName="['负面事件', '二类', '三类', '四类']" :xData="weekHotPointX"
            :barData="weekHotPointData"></BasicBar>
        </dv-border-box-12>
        <dv-border-box-12 style="height: 35%;">
          <el-row style="height: 100%;">
            <el-col :span="12" style="height: 100%;">
              <div style="width: 100%; height: 100%;">
                <Ring titleText="本周新增" :valueData="weekAddData1" :color="['#05fbff', '#ff2b05']"></Ring>
              </div>
            </el-col>
            <el-col :span="12" style="height: 100%;">
              <div style="width: 100%; height: 100%;">
                <Ring :valueData="weekAddData2" :color="['#ff6905', '#ff2b05']"></Ring>
              </div>
            </el-col>
          </el-row>
        </dv-border-box-12>
      </el-col>
      <el-col :span="7" style="height: 100%;">
        <dv-border-box-12 id="carousel">
          <span>实时热点榜</span>
          <div style="width: 90%; height: 90%;">
            <Carousel :header="['类型', '事件', '热度']" :data="hotpointData" :rowNum="8" :columnWidth="[50, 85, 200, 80]"
              :onClick="clickCarousel">
            </Carousel>
          </div>
        </dv-border-box-12>
      </el-col>
    </el-row>
    <el-row style="height: 30%;">
      <el-col :span="10" style="height: 100%;">
        <dv-border-box-12>
          <SmoothLine titleText="中大词条浏览月统计" :xData="monthEntryX" :valueData="monthEntryData" fontColor="white">
          </SmoothLine>
        </dv-border-box-12>
      </el-col>
      <el-col :span="7" style="height: 100%;">
        <dv-border-box-12>
          <BasicBar titleText="中大词条浏览周统计" :barNum="2" :barName="['负面事件', '热点事件']" :xData="weekEntryX"
            :barData="weekEntryData">
          </BasicBar>
        </dv-border-box-12>
      </el-col>
      <el-col :span="7" style="height: 100%;">
        <dv-border-box-12 id="carousel">
          <span>热度上升榜</span>
          <div style="width: 90%; height: 83%;">
            <Carousel :header="['类型', '事件', '速度']" :data="hotpointSpeed" :rowNum="5" :columnWidth="[50, 85, 200, 80]"
              :onClick="clickCarousel">
            </Carousel>
          </div>
        </dv-border-box-12>
      </el-col>
    </el-row>
  </dv-full-screen-container>
  <!-- </div> -->
</template>

<script>
// @ is an alias to /src
import StackedBar from '@/components/StackedBar.vue';
import Nightingale from '@/components/Nightingale.vue';
import BasicBar from '@/components/BasicBar.vue';
import SmoothLine from '@/components/SmoothLine.vue';
import Ring from '@/components/Ring.vue';
import Carousel from '@/components/Carousel.vue';
import { getHotPointList, getSpeedList } from '@/api/panel';

export default {
  name: 'HomeView',
  components: {
    StackedBar,
    Nightingale,
    BasicBar,
    SmoothLine,
    Ring,
    Carousel,
  },
  data() {
    return {
      stackedBarXData: ['1月', '2月', '3月', '4月', '5月', '6月'],
      stackedBarUserData: [30, 35, 37, 28, 43, 40],
      stackedBarSelfData: [10, 13, 10, 15, 8, 11],
      stackedBarMainData: [14, 11, 9, 8, 10, 9],
      nightinggaleData: [
        { name: '抖音', value: 20 },
        { name: 'B站', value: 10 },
        { name: '快手', value: 16 },
        { name: '公众号', value: 22 },
        { name: '微博', value: 20 },
        { name: '小红书', value: 11 },
        { name: '报社', value: 20 },
        { name: '集市', value: 13 },
        { name: '贴吧', value: 9 },
      ],
      weekHotPointX: ['4月28日', '4月29日', '4月30日', '5月1日', '5月2日', '5月3日', '5月4日'],
      weekHotPointData: [
        [120, 130, 125, 140, 250, 240, 230],
        [130, 124, 138, 119, 210, 202, 176],
        [106, 158, 148, 160, 207, 176, 194],
        [150, 144, 135, 142, 167, 175, 214]
      ],
      weekEntryX: ['4月二周', '4月三周', '4月四周', '4月五周', '5月一周'],
      weekEntryData: [
        [60, 65, 61, 32, 72],
        [43, 37, 57, 35, 52]
      ],
      monthEntryX: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
      monthEntryData: [64, 71, 84, 51, 54, 62, 59, 78, 94, 84, 74, 68],
      weekAddData1: [
        { name: '热点事件', value: 12 },
        { name: '负面事件', value: 3 },
      ],
      weekAddData2: [
        { name: '舆情预警', value: 12 },
        { name: '系统警告', value: 3 },
      ],
      hotpointData: [
        ['行1列1', '很长很长很长很长很长很长的数据', '行1列3'],
        ['行2列1', '行2列2', 23],
        ['行3列1', '行3列2', 43],
        ['行4列1', '行4列2', '行4列3'],
        ['行5列1', '行5列2', '行5列3'],
        ['行6列1', '行6列2', '行6列3'],
        ['行7列1', '行7列2', '行7列3'],
        ['行8列1', '行8列2', '行8列3'],
        ['行9列1', '行9列2', '行9列3'],
        ['负面事件', '行10列2', '行10列3']
      ],
      hotpointSpeed: [
        ['行1列1', '很长很长很长很长很长很长的数据', '行1列3'],
        ['行2列1', '行2列2', '行2列3'],
        ['行3列1', '行3列2', '行3列3'],
        ['行4列1', '行4列2', '行4列3'],
        ['行5列1', '行5列2', '行5列3'],
        ['行6列1', '行6列2', '行6列3'],
        ['行7列1', '行7列2', '行7列3'],
        ['行8列1', '行8列2', '行8列3'],
        ['行9列1', '行9列2', '行9列3'],
        ['负面事件', '行10列2', '行10列3']
      ],
    };
  },
  created() {
    // 获取热榜
    getHotPointList().then((res) => {
      if (res.status == 200) {
        this.hotpointData = res.data.data;
      }
    }).catch((err) => {
      console.log(err);
    })

    // 获取热度上升榜
    getSpeedList().then((res) => {
      if (res.status == 200) {
        this.hotpointSpeed = res.data.data;
      }
    }).catch((err) => {
      console.log(err);
    })
  },
  mounted() {

  },
  methods: {
    clickCarousel(config) {
      console.log(config.rowIndex);
      this.$root.topic = config.row[2];
      console.log(this.$root.topic);
      this.$router.push('/menu/topic');
    }
  }
}
</script>


<style>
#dv-full-screen-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  background-image: url('../../assets/background.jpg');
}

.title {
  color: white;
  font-size: 25px;
  font-weight: bold;
}

#carousel .border-box-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

#carousel span {
  padding-top: 1.5%;
  font-size: 18px;
  font-weight: bolder;
  font-family: sans-serif;
  color: white;
}
</style>