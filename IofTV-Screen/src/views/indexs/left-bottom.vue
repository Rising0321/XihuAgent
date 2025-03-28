<!--
 * @Author: daidai
 * @Date: 2022-03-01 09:43:37
 * @LastEditors: Please set LastEditors
 * @LastEditTime: 2022-09-09 11:40:22
 * @FilePath: \web-pc\src\pages\big-screen\view\indexs\left-bottom.vue
-->
<template>
  <div class="water-level-container">
    <ul class="water_level flex" v-if="pageflag">
      <li class="water_level-item" style="color: #00fdfa">
        <div class="water_level_value allnum">
          <dv-digital-flop :config="qiantangConfig" style="width:100%;height:100%;" />
        </div>
        <p>钱塘江闸口</p>
      </li>
      <li class="water_level-item" style="color: #07f7a8">
        <div class="water_level_value online">
          <dv-digital-flop :config="jinlongConfig" style="width:100%;height:100%;" />
        </div>
        <p>进龙河闸内</p>
      </li>
      <li class="water_level-item" style="color: #e3b337">
        <div class="water_level_value offline">
          <dv-digital-flop :config="jiuxiConfig" style="width:100%;height:100%;" />
        </div>
        <p>九溪闸内</p>
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
      waterLevelData: {},
      pageflag: true,
      timer: null,
      qiantangConfig: {
        number: [0],
        content: '{nt}',
        toFixed: 2,
        style: {
          ...style,
          fill: "#00fdfa",
        },
      },
      jinlongConfig: {
        number: [0],
        content: '{nt}',
        toFixed: 2,
        style: {
          ...style,
          fill: "#07f7a8",
        },
      },
      jiuxiConfig: {
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
      currentGET("water-level").then((res) => {
        if (!this.timer) {
          console.log("水位数据", res);
        }
        if (res.success) {
          this.waterLevelData = res.data;
          
          // Update the digital flop values with 2 decimal places
          this.qiantangConfig = {
            ...this.qiantangConfig,
            number: [parseFloat(res.data['钱塘江闸口'])]
          }
          this.jinlongConfig = {
            ...this.jinlongConfig,
            number: [parseFloat(res.data['进龙河闸内'])]
          }
          this.jiuxiConfig = {
            ...this.jiuxiConfig,
            number: [parseFloat(res.data['九溪闸内'])]
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
.water_level {
  li {
    flex: 1;

    p {
      text-align: center;
      height: 16px;
      font-size: 16px;
    }

    .water_level_value {
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
  }
}

.water-level-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
</style>