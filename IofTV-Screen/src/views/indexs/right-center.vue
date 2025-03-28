<!--
 * @Author: daidai
 * @Date: 2022-03-01 15:51:43
 * @LastEditors: Please set LastEditors
 * @LastEditTime: 2022-09-29 15:12:46
 * @FilePath: \web-pc\src\pages\big-screen\view\indexs\right-bottom.vue
-->
<template>
  <div class="right_center">
    <div class="chart-title">{{ currentTitle }}</div>
    <Echart
      id="rightCenter"
      :options="option"
      class="right_center_inner"
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
      currentDataType: 'hour', // 'hour' or 'day'
      hourlyData: [], // Top10小时收费客流数据
      dailyData: [], // Top10日收费客流数据
      currentTitle: 'Top10小时收费客流'
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
      console.log("Fetching top 10 visitor spot data...");
      
      // Clear any existing timers before fetching new data
      this.clearData();
      
      // Get hourly data
      currentGET("6-hour-spot-top10").then((hourRes) => {
        console.log("Hour spot data response:", hourRes);
        if (hourRes.success && hourRes.data && hourRes.data.length > 0) {
          this.hourlyData = hourRes.data;
          
          // Get daily data
          currentGET("7-day-spot-top10").then((dayRes) => {
            console.log("Day spot data response:", dayRes);
            if (dayRes.success && dayRes.data && dayRes.data.length > 0) {
              this.dailyData = dayRes.data;
              
              // 保存当前数据类型
              const prevDataType = this.currentDataType || 'hour';
              const prevTitle = this.currentTitle || 'Top10小时收费客流';
              
              // 只在初始加载时设置为小时数据
              if (!this.currentDataType) {
                this.currentDataType = 'hour';
                this.currentTitle = 'Top10小时收费客流';
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
              this.handleError(dayRes.msg || "Daily spot data is empty");
            }
          }).catch(error => {
            this.handleError('Failed to fetch daily spot data');
          });
        } else {
          this.handleError(hourRes.msg || "Hourly spot data is empty");
        }
      }).catch(error => {
        this.handleError('Failed to fetch hourly spot data');
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
      
      // Switch between hourly and daily data every 3 seconds
      this.switchTimer = setInterval(() => {
        if (this.currentDataType === 'hour') {
          this.currentDataType = 'day';
          this.currentTitle = 'Top10日收费客流';
        } else {
          this.currentDataType = 'hour';
          this.currentTitle = 'Top10小时收费客流';
        }
        console.log("Switching to:", this.currentTitle);
        this.updateChart();
      }, 3000); // Switch every 3 seconds
    },
    
    updateChart() {
      const currentData = this.currentDataType === 'hour' ? this.hourlyData : this.dailyData;
      
      if (!currentData || currentData.length === 0) {
        console.warn(`No data available for ${this.currentDataType} chart`);
        return;
      }
      
      console.log(`Updating chart with ${this.currentDataType} data:`, currentData.length);
      
      // 设置横坐标数据（地点名称）和纵坐标数据（客流量）
      const xData = currentData.map(item => item.spot);
      const yData = currentData.map(item => item.number);
      
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
      const yAxisMax = Math.ceil(dataMax * 1.2);
      const yAxisMin = 0;
      
      // 设置柱形图的颜色
      const barColors = this.currentDataType === 'hour' 
        ? ['#3DA9FC', '#90B4CE', '#5F6C7B'] // 小时数据颜色
        : ['#EF4565', '#F9CFC3', '#E16162']; // 日数据颜色
        
      // 渲染柱形图
      this.option = {
        backgroundColor: 'transparent',
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          },
          formatter: (params) => {
            const dataPoint = params[0];
            let valueFormat = dataPoint.value.toLocaleString() + '人';
            if (dataPoint.value >= 10000) {
              valueFormat = (dataPoint.value / 10000).toFixed(2) + '万人';
            }
            return `${dataPoint.name}<br/>${dataPoint.seriesName}: ${valueFormat}`;
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
            color: '#7EB7FD',
            formatter: function(value) {
              if (value >= 10000) {
                return (value / 10000).toFixed(1) + '万';
              }
              return value;
            }
          }
        },
        series: [
          {
            name: this.currentDataType === 'hour' ? '小时客流量' : '日客流量',
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
              color: '#fff',
              formatter: function(params) {
                if (params.value >= 10000) {
                  return (params.value / 10000).toFixed(1) + '万';
                }
                return params.value;
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
.right_center {
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
  
  .right_center_inner {
    width: 100%;
    height: 100%;
  }
}
</style>