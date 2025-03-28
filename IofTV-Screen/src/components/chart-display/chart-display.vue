<template>
  <div class="chart-display">
    <!-- 杭州地图底图 -->
    <div class="map-container">
      <hangzhou-map></hangzhou-map>
    </div>
    <!-- 图表显示区域 -->
    <transition name="fade">
      <div v-if="currentComponent" class="chart-modal">
        <div class="modal-content">
          <span class="close-btn" @click="closeChart">✕</span>
          <div class="modal-body">
            <component
              :is="currentComponent"
              class="chart-component"
            ></component>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import LeftTop from '@/views/indexs/left-top.vue'
import LeftCenter from '@/views/indexs/left-center.vue'
import LeftBottom from '@/views/indexs/left-bottom.vue'
import RightTop from '@/views/indexs/right-top.vue'
import RightCenter from '@/views/indexs/right-center.vue'
import RightBottom from '@/views/indexs/right-bottom.vue'
import CenterBottom from '@/views/indexs/center-bottom.vue'
import HangzhouMap from '@/components/hangzhou-map/hangzhou-map.vue'

export default {
  name: 'ChartDisplay',
  components: {
    'hangzhou-map': HangzhouMap
  },
  data() {
    return {
      currentChart: '',
      componentMap: {
        'left-top': LeftTop,
        'left-center': LeftCenter,
        'left-bottom': LeftBottom,
        'right-top': RightTop,
        'right-center': RightCenter,
        'right-bottom': RightBottom,
        'center-bottom': CenterBottom
      }
    }
  },
  computed: {
    currentComponent() {
      return this.componentMap[this.currentChart]
    }
  },
  methods: {
    updateChart(chartId) {
      this.currentChart = chartId
    },
    closeChart() {
      this.currentChart = ''
    }
  }
}
</script>

<style lang="scss" scoped>
.chart-display {
  position: fixed;
  left: 100px;
  right: 0;
  top: 0;
  bottom: 0;

  .map-container {
    position: absolute;
    left: 100px;
    right: 0;
    top: 80px;
    bottom: 20px;
    z-index: 0;
    overflow: hidden;
  }
}

.chart-modal {
  position: fixed;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 45%;
  min-width: 600px;
  height: 45%;
  min-height: 400px;
  z-index: 100;
  
  .modal-content {
    position: relative;
    width: 100%;
    height: 100%;
    background: rgba(13, 19, 35, 0.85);
    backdrop-filter: blur(10px);
    border-radius: 10px;
    border: 1px solid rgba(0, 162, 255, 0.3);
    box-shadow: 0 2px 20px 0 rgba(0, 162, 255, 0.2);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .close-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    cursor: pointer;
    font-size: 18px;
    transition: all 0.3s ease;
    color: rgba(255, 255, 255, 0.8);
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 4px;
    z-index: 1;

    &:hover {
      color: #fff;
      background: rgba(255, 255, 255, 0.1);
    }
  }

  .modal-body {
    flex: 1;
    height: 100%;
    padding: 20px;
    overflow: hidden;
  }

  .chart-component {
    width: 100%;
    height: 100%;
  }
}

// 过渡动画
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translate(-50%, -45%);
}

.fade-enter-to,
.fade-leave-from {
  opacity: 1;
  transform: translate(-50%, -50%);
}
</style> 