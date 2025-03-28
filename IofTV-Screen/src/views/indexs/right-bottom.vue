<!--
 * @Author: daidai
 * @Date: 2022-03-01 15:27:58
 * @LastEditors: Please set LastEditors
 * @LastEditTime: 2022-05-07 11:24:14
 * @FilePath: \web-pc\src\pages\big-screen\view\indexs\right-bottom.vue
-->
<template>
  <div class="right_bottom">
    <div class="chart-title">{{ currentTitle }}</div>
    <Echart
      id="rightBottom"
      :options="option"
      class="right_bottom_inner"
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
      option: {},
      pageflag: false,
      timer: null,
      switchTimer: null,
      currentDataType: 'congestion', // 'congestion' 拥堵指数 or 'speed' 平均速度
      congestionData: [], // Top10拥堵路段数据
      speedData: [], // 周边平均速度数据
      currentTitle: 'Top10拥堵路段'
    };
  },
  created() {
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
      if (this.switchTimer) {
        clearInterval(this.switchTimer);
        this.switchTimer = null;
      }
    },
    getData() {
      this.pageflag = true;
      console.log("Fetching traffic data...");
      
      // Clear any existing timers before fetching new data
      this.clearData();
      
      // Get congestion data
      currentGET("8-road-delay-top10").then((congestionRes) => {
        console.log("Congestion data response:", congestionRes);
        if (congestionRes.success && congestionRes.data && congestionRes.data.length > 0) {
          this.congestionData = congestionRes.data;
          
          // Get speed data
          currentGET("9-road-delay-speed").then((speedRes) => {
            console.log("Speed data response:", speedRes);
            if (speedRes.success && speedRes.data && speedRes.data.length > 0) {
              this.speedData = speedRes.data;
              
              // 保存当前数据类型
              const prevDataType = this.currentDataType || 'congestion';
              const prevTitle = this.currentTitle || 'Top10拥堵路段';
              
              // 只在初始加载时设置为拥堵路段数据
              if (!this.currentDataType) {
                this.currentDataType = 'congestion';
                this.currentTitle = 'Top10拥堵路段';
              } else {
                // 保持现有数据类型
                this.currentDataType = prevDataType;
                this.currentTitle = prevTitle;
              }
              
              this.updateChart();
              
              // 只在没有正在运行的定时器时启动
              if (!this.switchTimer) {
                this.startDataSwitchTimer();
              }
              
              // 只在没有正在运行的定时器时启动
              if (!this.timer) {
                this.switper();
              }
            } else {
              this.handleError(speedRes.msg || "Speed data is empty");
            }
          }).catch(error => {
            this.handleError('Failed to fetch speed data');
          });
        } else {
          this.handleError(congestionRes.msg || "Congestion data is empty");
        }
      }).catch(error => {
        this.handleError('Failed to fetch congestion data');
      });
    },
    
    handleError(msg) {
      this.pageflag = false;
      this.$Message({
        text: msg || 'An error occurred',
        type: "warning",
      });
    },
    
    startDataSwitchTimer() {
      // Clear any existing timer first
      if (this.switchTimer) {
        clearInterval(this.switchTimer);
        this.switchTimer = null;
      }
      
      console.log("Starting data switch timer");
      
      // Switch between congestion and speed data every 3 seconds
      this.switchTimer = setInterval(() => {
        if (this.currentDataType === 'congestion') {
          this.currentDataType = 'speed';
          this.currentTitle = '周边平均速度';
        } else {
          this.currentDataType = 'congestion';
          this.currentTitle = 'Top10拥堵路段';
        }
        console.log("Switching to:", this.currentTitle);
        this.updateChart();
      }, 3000); // Switch every 3 seconds
    },
    
    updateChart() {
      if (this.currentDataType === 'congestion') {
        this.renderCongestionChart();
      } else {
        this.renderSpeedChart();
      }
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
    
    // 渲染拥堵路段柱形图
    renderCongestionChart() {
      if (!this.congestionData || this.congestionData.length === 0) {
        console.warn("No congestion data available");
        return;
      }
      
      console.log("Updating chart with congestion data:", this.congestionData.length);
      
      // 处理路段名称，只显示冒号前的部分
      const xData = this.congestionData.map(item => {
        const roadName = item['路段名称'];
        const colonIndex = roadName.indexOf(':');
        if (colonIndex !== -1) {
          return roadName.substring(0, colonIndex);
        }
        return roadName;
      });
      
      const yData = this.congestionData.map(item => item['小时平均拥堵指数']);
      
      // 计算Y轴最大值，使其为数据最大值的1.2倍
      const dataMax = Math.max(...yData);
      const yAxisMax = Math.ceil(dataMax * 1.2);
      const yAxisMin = 0;
      
      // 设置柱形图的颜色
      const barColors = ['#F56C6C', '#E6A23C', '#F2D22D'];
      
      this.option = {
        backgroundColor: 'transparent',
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          },
          formatter: (params) => {
            const dataPoint = params[0];
            const item = this.congestionData[dataPoint.dataIndex];
            return `${item['路段名称']}<br/>${dataPoint.seriesName}: ${dataPoint.value.toFixed(2)}`;
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
            rotate: 45,
            formatter: function(value) {
              if(value.length > 8){
                return value.substring(0, 8) + '...';
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
            name: '拥堵指数',
            type: 'bar',
            data: yData,
            barWidth: '40%',
            itemStyle: {
              color: function(params) {
                // 根据索引选择不同的颜色
                const colorIndex = params.dataIndex % barColors.length;
                return barColors[colorIndex];
              },
              borderRadius: [4, 4, 0, 0]
            },
            label: {
              show: true,
              position: 'top',
              color: '#fff',
              formatter: function(params) {
                return params.value.toFixed(2);
              }
            }
          }
        ]
      };
    },
    
    // 渲染平均速度折线图
    renderSpeedChart() {
      if (!this.speedData || this.speedData.length === 0) {
        console.warn("No speed data available");
        return;
      }
      
      console.log("Updating chart with speed data:", this.speedData.length);
      
      // 反转数组，使最新的数据显示在右侧
      const reversedData = [...this.speedData].reverse();
      
      // 处理时间标签，只显示小时部分
      const xData = reversedData.map(item => {
        const time = item['Time'];
        // 提取时间中的小时部分
        const timeMatch = time.match(/\d{2}:\d{2}:\d{2}$/);
        if (timeMatch) {
          return timeMatch[0].substring(0, 5); // HH:MM
        }
        return time;
      });
      
      const yData = reversedData.map(item => item['小时平均速度']);
      
      // 计算Y轴范围
      const minSpeed = Math.min(...yData) * 0.9;
      const maxSpeed = Math.max(...yData) * 1.1;
      
      this.option = {
        backgroundColor: 'transparent',
        tooltip: {
          trigger: 'axis',
          formatter: (params) => {
            const dataPoint = params[0];
            const item = reversedData[dataPoint.dataIndex];
            return `${item['Time']}<br/>${dataPoint.seriesName}: ${dataPoint.value.toFixed(2)} km/h`;
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
            color: '#7EB7FD'
          }
        },
        yAxis: {
          type: 'value',
          min: Math.floor(minSpeed),
          max: Math.ceil(maxSpeed),
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
            color: '#7EB7FD',
            formatter: '{value} km/h'
          }
        },
        series: [
          {
            name: '平均速度',
            type: 'line',
            data: yData,
            smooth: true,
            symbol: 'circle',
            symbolSize: 8,
            itemStyle: {
              color: '#5ECBC8'
            },
            lineStyle: {
              width: 3,
              color: new graphic.LinearGradient(0, 0, 1, 0, [
                {offset: 0, color: '#5ECBC8'},
                {offset: 1, color: '#4670F8'}
              ])
            },
            areaStyle: {
              color: new graphic.LinearGradient(0, 0, 0, 1, [
                {
                  offset: 0,
                  color: 'rgba(94,203,200,0.5)'
                },
                {
                  offset: 1,
                  color: 'rgba(94,203,200,0.1)'
                }
              ])
            },
            label: {
              show: true,
              position: 'top',
              color: '#fff',
              formatter: function(params) {
                return params.value.toFixed(1);
              }
            }
          }
        ]
      };
    }
  }
};
</script>
<style lang='scss' scoped>
.right_bottom {
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
  
  .right_bottom_inner {
    width: 100%;
    height: 100%;
  }
}
</style>