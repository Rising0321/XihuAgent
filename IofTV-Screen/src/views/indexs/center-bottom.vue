<template>
  <div class="center_bottom">
    <div class="chart-title">Top10日车位情况</div>
    <Echart
      id="centerBottom"
      :options="options"
      class="center_bottom_inner"
      v-if="pageflag"
      ref="charts"
    />
    <Reacquire v-else @onclick="getData" style="line-height: 200px">
      重新获取
    </Reacquire>
  </div>
</template>

<script>
import { currentGET } from "api/modules";
import { graphic } from "echarts";

export default {
  data() {
    return {
      options: {},
      pageflag: false,
      timer: null,
      carParkData: [] // Top10日车位数据
    };
  },
  mounted() {
    this.getData();
  },
  beforeDestroy() {
    this.clearData();
  },
  methods: {
    clearData() {
      console.log("Clearing timers");
      if (this.timer) {
        clearInterval(this.timer);
        this.timer = null;
      }
    },
    getData() {
      this.pageflag = true;
      console.log("Fetching top 10 car park data...");
      
      // Clear any existing timers before fetching new data
      this.clearData();
      
      // Get car park data
      currentGET("10-car-park-top10").then((res) => {
        console.log("Car park data response:", res);
        if (res.success && res.data && res.data.length > 0) {
          this.carParkData = res.data;
          this.updateChart();
          
          // 只在没有正在运行的定时器时启动
          if (!this.timer) {
            this.switper();
          }
        } else {
          this.handleError(res.msg || "Car park data is empty");
        }
      }).catch(error => {
        this.handleError('Failed to fetch car park data');
      });
    },
    
    handleError(msg) {
      this.pageflag = false;
      this.$Message({
        text: msg || 'An error occurred',
        type: "warning",
      });
    },
    
    updateChart() {
      if (!this.carParkData || this.carParkData.length === 0) {
        console.warn("No car park data available");
        return;
      }
      
      console.log("Updating chart with car park data:", this.carParkData.length);
      
      // 设置横坐标数据（停车场名称）和纵坐标数据（车辆数量）
      const xData = this.carParkData.map(item => item.pk_name);
      const yData = this.carParkData.map(item => item.count);
      
      this.renderChart(xData, yData);
    },
    
    //轮询
    switper() {
      if (this.timer) {
        return;
      }
      let looper = () => {
        this.getData();
      };
      this.timer = setInterval(looper, this.$store.state.setting.echartsAutoTime);
    },
    
    renderChart(xData, yData) {
      // 计算Y轴最大值，使其为数据最大值的1.2倍
      const dataMax = Math.max(...yData);
      const yAxisMax = Math.ceil(dataMax * 1.2) || 10; // 如果全为0，设置最大值为10
      const yAxisMin = 0;
      
      // 设置柱形图的颜色
      const barColors = ['#3EACE5', '#956FD4', '#F0437B'];
        
      // 渲染柱形图
      this.options = {
        backgroundColor: 'transparent',
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          },
          formatter: (params) => {
            const dataPoint = params[0];
            return `${dataPoint.name}<br/>${dataPoint.seriesName}: ${dataPoint.value}辆`;
          }
        },
        grid: {
          top: '15%',
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: xData,
          axisLine: {
            lineStyle: {
              color: 'rgba(31,99,163,.1)'
            }
          },
          axisLabel: {
            color: '#7EB7FD',
            fontSize: 10,
            interval: 0,
            rotate: 45, // 旋转标签以避免重叠
            formatter: function(value) {
              if(value.length > 6){
                return value.substring(0, 6) + '...';
              }
              return value;
            }
          }
        },
        yAxis: {
          type: 'value',
          min: yAxisMin,
          max: yAxisMax,
          splitLine: {
            show: true,
            lineStyle: {
              color: 'rgba(31,99,163,.2)'
            }
          },
          axisLine: {
            lineStyle: {
              color: 'rgba(31,99,163,.1)'
            }
          },
          axisLabel: {
            color: '#7EB7FD'
          }
        },
        series: [
          {
            name: '车辆数量',
            type: 'bar',
            data: yData,
            barWidth: '30%',
            itemStyle: {
              color: function(params) {
                // 根据索引选择不同的颜色
                const colorIndex = params.dataIndex % barColors.length;
                return barColors[colorIndex];
              },
              borderRadius: [4, 4, 0, 0] // 设置柱形图上方边角为圆角
            },
            label: {
              show: true,
              position: 'top',
              color: '#fff'
            }
          }
        ]
      };
    }
  }
};
</script>
<style lang="scss" scoped>
.center_bottom {
  position: relative;
  width: 100%;
  height: 100%;
  
  .chart-title {
    position: absolute;
    top: 5px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 16px;
    color: #ffffff;
    z-index: 10;
    font-weight: 500;
  }
  
  .center_bottom_inner {
    width: 100%;
    height: 100%;
  }
}
</style>
