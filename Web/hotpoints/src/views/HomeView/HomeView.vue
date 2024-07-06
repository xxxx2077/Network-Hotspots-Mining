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
          <BasicBar titleText="本周热度数据统计" :barNum="4" :barName="['舆论预警', '负面事件', '校外热点', '校内热点']" :xData="weekHotPointX"
            :barData="weekHotPointData" :flag="weekHotPointFlag"></BasicBar>
        </dv-border-box-12>
        <dv-border-box-12 style="height: 35%;">
          <el-row style="height: 100%;">
            <el-col :span="12" style="height: 100%;">
              <div style="width: 100%; height: 100%;">
                <Ring titleText="本周新增" :valueData="weekAddData1" :color="['#05fbff', '#ff2b05']" :flag="weekAddFlag1">
                </Ring>
              </div>
            </el-col>
            <el-col :span="12" style="height: 100%;">
              <div style="width: 100%; height: 100%;">
                <Ring :valueData="weekAddData2" :color="['#ff6905', '#ff2b05']" :flag="weekAddFlag2"></Ring>
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
              :flag="hotpointDataFlag" :onClick="clickHotList">
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
            :barData="weekEntryData" :flag="weekEntryFlag">
          </BasicBar>
        </dv-border-box-12>
      </el-col>
      <el-col :span="7" style="height: 100%;">
        <dv-border-box-12 id="carousel">
          <span>热度上升榜</span>
          <div style="width: 90%; height: 83%;">
            <Carousel :header="['类型', '事件', '速度']" :data="hotpointSpeed" :rowNum="5" :columnWidth="[50, 85, 200, 80]"
              :flag="hotpointSpeedFlag" :onClick="clickSpeedList">
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
import { getHotPointList, getSpeedList, getClassHotVal, getWeekAdded } from '@/api/panel';

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
      weekHotPointX: [],
      weekHotPointData: [],
      weekHotPointFlag: false,
      weekEntryX: ['4月二周', '4月三周', '4月四周', '4月五周', '5月一周'],
      weekEntryData: [
        [60, 65, 61, 32, 72],
        [43, 37, 57, 35, 52]
      ],
      weekEntryFlag: false,
      monthEntryX: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
      monthEntryData: [64, 71, 84, 51, 54, 62, 59, 78, 94, 84, 74, 68],
      weekAddData1: [],
      weekAddFlag1: false,
      weekAddData2: [],
      weekAddFlag2: false,
      hotpointRawData: [],
      hotpointData: [['', '', '']],
      hotpointDataFlag: false,
      hotpointRawSpeed: [],
      hotpointSpeed: [['', '', '']],
      hotpointSpeedFlag: false,
    };
  },
  created() {

  },
  mounted() {
    // 获取热榜
    getHotPointList().then((res) => {
      if (res.status == 200) {
        this.hotpointRawData = res.data.data;
        // 整理成二维数组
        this.hotpointData.pop();
        for (let obj of this.hotpointRawData) {
          const arr = Object.keys(obj).map(item => obj[item]);
          arr.shift();
          this.hotpointData.push(arr);
        }
        // console.log(this.hotpointData);
        this.hotpointDataFlag = !this.hotpointDataFlag;
      }
    }).catch((err) => {
      console.log(err);
    })

    // 获取热度上升榜
    getSpeedList().then((res) => {
      if (res.status == 200) {
        this.hotpointRawSpeed = res.data.data;
        // 整理成二维数组
        this.hotpointSpeed.pop();
        for (let obj of this.hotpointRawSpeed) {
          const arr = Object.keys(obj).map(item => obj[item]);
          arr.shift();
          this.hotpointSpeed.push(arr);
        }
        this.hotpointSpeedFlag = !this.hotpointSpeedFlag;
      }
    }).catch((err) => {
      console.log(err);
    })

    // 事件类别热度
    getClassHotVal().then((res) => {
      if (res.status == 200) {
        const arr_1 = [], arr_2 = [], arr_3 = [], arr_4 = [];
        res.data.data.forEach(obj => {
          arr_1.push(obj["1"]);
          arr_2.push(obj["2"]);
          arr_3.push(obj["3"]);
          arr_4.push(obj["4"]);
          this.weekHotPointX.push(obj.date);
        })
        this.weekHotPointData.push(arr_1);
        this.weekHotPointData.push(arr_2);
        this.weekHotPointData.push(arr_3);
        this.weekHotPointData.push(arr_4);
        this.weekHotPointFlag = !this.weekHotPointFlag;
      }
    }).catch((err) => {
      console.log(err);
    })

    // 获取本周新增
    getWeekAdded().then((res) => {
      if (res.status == 200) {
        this.weekAddData1 = [];
        this.weekAddData1.push({ name: '热点事件', value: res.data.data.hotspot });
        this.weekAddData1.push({ name: '负面事件', value: res.data.data.negative });
        this.weekAddFlag1 = !this.weekAddFlag1;
        this.weekAddData2 = [];
        this.weekAddData2.push({ name: '舆情预警', value: res.data.data.prewarning });
        this.weekAddData2.push({ name: '系统警告', value: res.data.data.warning });
        this.weekAddFlag2 = !this.weekAddFlag2;
        console.log(this.weekAddFlag1);
        console.log(this.weekAddFlag2);
      }
    }).catch((err) => {
      console.log(err);
    })
  },
  methods: {
    clickHotList(config) {
      const index = config.rowIndex;
      this.$router.push({ name: 'Topic', params: { id: this.hotpointRawData[index].id } });
    },
    clickSpeedList(config) {
      const index = config.rowIndex;
      this.$router.push({ name: 'Topic', params: { id: this.hotpointRawSpeed[index].id } });
    }
  }
}
</script>


<style scoped>
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

:deep(#carousel .border-box-content) {
  display: flex;
  flex-direction: column;
  align-items: center;
}

:deep(#carousel span) {
  padding-top: 1.5%;
  font-size: 18px;
  font-weight: bolder;
  font-family: sans-serif;
  color: white;
}

:deep(.row-item:hover) {
  cursor: pointer;
}
</style>