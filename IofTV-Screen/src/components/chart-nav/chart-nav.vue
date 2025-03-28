<template>
  <div class="chart-nav">
    <div class="nav-header">西湖监测指标</div>
    <div class="nav-list">
      <div
        v-for="(item, index) in chartList"
        :key="index"
        class="nav-item"
        :class="{ active: currentChart === item.id }"
        @click="handleChartClick(item)"
      >
        <div class="indicator">
          <span class="value" :class="item.status">{{ item.value }}</span>
          <span class="unit">{{ item.unit }}</span>
        </div>
        <span class="title">{{ item.title }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ChartNav',
  data() {
    return {
      currentChart: '',
      chartList: [
        {
          id: 'left-top',
          title: '西湖水质',
          value: '6.03',
          unit: 'pH',
          status: 'normal',
        },
        {
          id: 'left-center',
          title: '西湖空气',
          value: '22.7',
          unit: '℃',
          status: 'normal',
        },
        {
          id: 'left-bottom',
          title: '西湖水位',
          value: '7.28',
          unit: 'm',
          status: 'normal',
        },
        {
          id: 'right-top',
          title: '全域客流',
          value: '4.27',
          unit: '万人',
          status: 'good',
        },
        {
          id: 'right-center',
          title: '收费客流',
          value: '1.83',
          unit: '万人',
          status: 'good',
        },
        {
          id: 'right-bottom',
          title: '延误指数',
          value: '2.69',
          unit: '分',
          status: 'warning',
        },
        {
          id: 'center-bottom',
          title: '车位情况',
          value: '73',
          unit: '%',
          status: 'warning',
        }
      ]
    }
  },
  methods: {
    handleChartClick(item) {
      this.currentChart = item.id
      this.$emit('chart-change', item.id)
    }
  }
}
</script>

<style lang="scss" scoped>
.chart-nav {
  position: fixed;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 100px;
  background: rgba(0, 12, 23, 0.7);
  border-radius: 0 4px 4px 0;
  padding: 15px 0 10px;
  z-index: 100;
  box-shadow: 0 0 15px rgba(0, 100, 255, 0.2);
  border-right: 1px solid rgba(0, 180, 255, 0.3);

  .nav-header {
    color: rgba(0, 180, 255, 0.8);
    font-size: 13px;
    text-align: center;
    margin-bottom: 10px;
    font-weight: bold;
    padding: 0 8px;
    line-height: 1.4;
  }

  .nav-list {
    .nav-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 12px 5px;
      cursor: pointer;
      transition: all 0.3s;
      color: #fff;
      border-top: 1px solid rgba(0, 60, 120, 0.5);

      &:hover {
        background: rgba(0, 100, 180, 0.2);
      }

      &.active {
        background: rgba(0, 120, 200, 0.3);
        border-left: 3px solid #00a8ff;
      }

      .indicator {
        margin-bottom: 5px;
        display: flex;
        align-items: baseline;
        
        .value {
          font-size: 16px;
          font-weight: bold;
          
          &.normal {
            color: #00ffff;
          }
          
          &.good {
            color: #00ff8d;
          }
          
          &.warning {
            color: #ff9800;
          }
          
          &.danger {
            color: #ff3d00;
          }
        }
        
        .unit {
          font-size: 10px;
          margin-left: 2px;
          opacity: 0.7;
        }
      }

      .title {
        font-size: 12px;
        text-align: center;
        color: rgba(255, 255, 255, 0.8);
        padding: 0 2px;
      }
    }
  }
}
</style> 