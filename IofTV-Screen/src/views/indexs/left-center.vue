<!--
 * @Author: daidai
 * @Date: 2022-02-28 16:16:42
 * @LastEditors: Please set LastEditors
 * @LastEditTime: 2022-10-25 09:18:22
 * @FilePath: \web-pc\src\pages\big-screen\view\indexs\left-center.vue
-->
<template>
  <div class="air-quality-container">
    <ul class="air_quality flex" v-if="pageflag">
      <li class="air_quality-item" style="color: #00fdfa">
        <div class="air_quality_value allnum">
          <dv-digital-flop :config="so2Config" style="width:100%;height:100%;" />
        </div>
        <p>SO2</p>
      </li>
      <li class="air_quality-item" style="color: #07f7a8">
        <div class="air_quality_value online">
          <dv-digital-flop :config="no2Config" style="width:100%;height:100%;" />
        </div>
        <p>NO2</p>
      </li>
      <li class="air_quality-item" style="color: #e3b337">
        <div class="air_quality_value offline">
          <dv-digital-flop :config="o3Config" style="width:100%;height:100%;" />
        </div>
        <p>O3</p>
      </li>
      <li class="air_quality-item" style="color: #f5023d">
        <div class="air_quality_value laramnum">
          <dv-digital-flop :config="coConfig" style="width:100%;height:100%;" />
        </div>
        <p>CO</p>
      </li>
    </ul>
    <ul class="air_quality flex mt-10" v-if="pageflag">
      <li class="air_quality-item" style="color: #00fdfa">
        <div class="air_quality_value allnum">
          <dv-digital-flop :config="aqiConfig" style="width:100%;height:100%;" />
        </div>
        <p>AQI</p>
      </li>
      <li class="air_quality-item" style="color: #07f7a8">
        <div class="air_quality_value online">
          <dv-digital-flop :config="pm25Config" style="width:100%;height:100%;" />
        </div>
        <p>PM2.5</p>
      </li>
      <li class="air_quality-item" style="color: #e3b337">
        <div class="air_quality_value offline">
          <dv-digital-flop :config="pm10Config" style="width:100%;height:100%;" />
        </div>
        <p>PM10</p>
      </li>
    </ul>
    <Reacquire v-else @onclick="getData" style="line-height:200px">
      重新获取
    </Reacquire>
  </div>
</template>

<script>
import { currentGET } from 'api/modules'
let style = {
  fontSize: 24
}

export default {
  data() {
    return {
      airQualityData: {},
      pageflag: true,
      timer: null,
      so2Config: {
        number: [0],
        content: '{nt}',
        toFixed: 2,
        style: {
          ...style,
          fill: "#00fdfa",
        },
      },
      no2Config: {
        number: [0],
        content: '{nt}',
        toFixed: 2,
        style: {
          ...style,
          fill: "#07f7a8",
        },
      },
      o3Config: {
        number: [0],
        content: '{nt}',
        toFixed: 2,
        style: {
          ...style,
          fill: "#e3b337",
        },
      },
      coConfig: {
        number: [0],
        content: '{nt}',
        toFixed: 2,
        style: {
          ...style,
          fill: "#f5023d",
        },
      },
      aqiConfig: {
        number: [0],
        content: '{nt}',
        toFixed: 2,
        style: {
          ...style,
          fill: "#00fdfa",
        },
      },
      pm25Config: {
        number: [0],
        content: '{nt}',
        toFixed: 2,
        style: {
          ...style,
          fill: "#07f7a8",
        },
      },
      pm10Config: {
        number: [0],
        content: '{nt}',
        toFixed: 2,
        style: {
          ...style,
          fill: "#e3b337",
        },
      }
    };
  },
  created() {
    this.getData()
  },
  mounted() {
  },
  beforeDestroy() {
    this.clearData()
  },
  methods: {
    clearData() {
      if (this.timer) {
        clearInterval(this.timer)
        this.timer = null
      }
    },
    getData() {
      this.pageflag = true;
      currentGET("air-quality").then((res) => {
        if (!this.timer) {
          console.log("空气质量数据", res);
        }
        if (res.success) {
          this.airQualityData = res.data;
          
          // Update the digital flop values with 2 decimal places
          this.so2Config = {
            ...this.so2Config,
            number: [parseFloat(res.data.SO2)]
          }
          this.no2Config = {
            ...this.no2Config,
            number: [parseFloat(res.data.NO2)]
          }
          this.o3Config = {
            ...this.o3Config,
            number: [parseFloat(res.data.O3)]
          }
          this.coConfig = {
            ...this.coConfig,
            number: [parseFloat(res.data.CO)]
          }
          this.aqiConfig = {
            ...this.aqiConfig,
            number: [parseFloat(res.data.AQI)]
          }
          this.pm25Config = {
            ...this.pm25Config,
            number: [parseFloat(res.data['PM2.5'])]
          }
          this.pm10Config = {
            ...this.pm10Config,
            number: [parseFloat(res.data.PM10)]
          }
          
          this.switper()
        } else {
          this.pageflag = false;
          this.$Message.warning(res.msg);
        }
      });
    },
    //轮询
    switper() {
      if (this.timer) {
        return
      }
      let looper = (a) => {
        this.getData()
      };
      this.timer = setInterval(looper, this.$store.state.setting.echartsAutoTime);
    },
  },
};
</script>
<style lang='scss' scoped>
.air_quality {
  li {
    flex: 1;

    p {
      text-align: center;
      height: 16px;
      font-size: 16px;
    }

    .air_quality_value {
      width: 100px;
      height: 100px;
      text-align: center;
      line-height: 100px;
      font-size: 22px;
      margin: 20px auto 10px;
      background-size: cover;
      background-position: center center;
      position: relative;

      &::before {
        content: '';
        position: absolute;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
      }

      &.bgdonghua::before {
        animation: rotating 14s linear infinite;
      }
    }

    .allnum {
      &::before {
        background-image: url("../../assets/img/left_top_lan.png");
      }
    }

    .online {
      &::before {
        background-image: url("../../assets/img/left_top_lv.png");
      }
    }

    .offline {
      &::before {
        background-image: url("../../assets/img/left_top_huang.png");
      }
    }

    .laramnum {
      &::before {
        background-image: url("../../assets/img/left_top_hong.png");
      }
    }
  }
}

.mt-10 {
  margin-top: 10px;
}
</style>