<!--
 * @Author: daidai
 * @Date: 2022-03-01 14:13:04
 * @LastEditors: Please set LastEditors
 * @LastEditTime: 2022-09-27 15:04:49
 * @FilePath: \web-pc\src\pages\big-screen\view\indexs\right-top.vue
-->
<template>
  <div class="visitor-flow-container">
    <div class="chart-title">{{ currentTitle }}</div>
    <Echart
      id="rightTop"
      :options="option"
      class="right_top_inner"
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
      hourlyData: [], // Data for hourly visitor flow
      dailyData: [], // Data for daily visitor flow
      currentTitle: '小时全域客流'
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
      console.log("Fetching visitor flow data...");
      
      // Clear any existing timers before fetching new data
      this.clearData();
      
      // Get hourly data
      currentGET("hour-west-lake").then((hourRes) => {
        console.log("Hour data response:", hourRes);
        if (hourRes.success && hourRes.data && hourRes.data.length > 0) {
          this.hourlyData = hourRes.data;
          
          // Get daily data
          currentGET("day-west-lake").then((dayRes) => {
            console.log("Day data response:", dayRes);
            if (dayRes.success && dayRes.data && dayRes.data.length > 0) {
              this.dailyData = dayRes.data;
              
              // 保存当前数据类型
              const prevDataType = this.currentDataType || 'hour';
              const prevTitle = this.currentTitle || '小时全域客流';
              
              // 只在初始加载时设置为小时数据
              if (!this.currentDataType) {
                this.currentDataType = 'hour';
                this.currentTitle = '小时全域客流';
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
              this.handleError(dayRes.msg || "Daily data is empty");
            }
          }).catch(error => {
            this.handleError('Failed to fetch daily data');
          });
        } else {
          this.handleError(hourRes.msg || "Hourly data is empty");
        }
      }).catch(error => {
        this.handleError('Failed to fetch hourly data');
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
          this.currentTitle = '日全域客流';
        } else {
          this.currentDataType = 'hour';
          this.currentTitle = '小时全域客流';
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
      
      const xData = currentData.map(item => item.time);
      const yData = currentData.map(item => item.value);
      
      this.renderChart(xData, yData);
    },
    
    //轮询
    switper() {
      // 只在定时器不存在时创建
      if (this.timer) {
        console.log("Refresh timer already exists, not creating another one");
        return;
      }
      
      console.log("Starting data refresh timer");
      let looper = (a) => {
        this.getData();
      };
      this.timer = setInterval(
        looper,
        this.$store.state.setting.echartsAutoTime
      );
      
      if (this.$refs.charts) {
        let myChart = this.$refs.charts.chart;
        // 移除现有事件监听器以避免重复
        myChart.off('mouseover');
        myChart.off('mouseout');
        
        // 添加新的事件监听器
        myChart.on("mouseover", (params) => {
          console.log("Chart mouseover - clearing timers");
          this.clearData();
        });
        
        myChart.on("mouseout", (params) => {
          console.log("Chart mouseout - restarting timers");
          // Only restart timers, don't reload data
          if (!this.switchTimer) {
            this.startDataSwitchTimer();
          }
          if (!this.timer) {
            // Start refresh timer but don't immediately refresh
            this.switper();
          }
        });
      }
    },
    
    renderChart(xData, yData) {
      // Calculate y-axis min and max for better display
      const maxValue = Math.max(...yData);
      const minValue = Math.min(...yData);
      // Calculate a reasonable range to make chart variations visible
      const range = maxValue - minValue;
      // Set y-axis min to be slightly below the minimum value (about 10% of the range)
      const yAxisMin = Math.max(0, minValue - range * 0.1);
      // Set y-axis max to be slightly above the maximum value
      const yAxisMax = maxValue + range * 0.1;
      
      this.option = {
        xAxis: {
          type: "category",
          data: xData,
          boundaryGap: false, // Start from origin
          splitLine: {
            show: true,
            lineStyle: {
              color: "rgba(31,99,163,.2)",
            },
          },
          axisLine: {
            lineStyle: {
              color: "rgba(31,99,163,.1)",
            },
          },
          axisLabel: {
            color: "#7EB7FD",
            fontWeight: "500",
            formatter: (value) => {
              if (this.currentDataType === 'hour') {
                // For hourly data, show HH:MM format
                return value.substring(11, 16); // Extract HH:MM from YYYY-MM-DD HH:MM:SS
              } else {
                // For daily data, show MM-DD format
                return value.substring(5, 10); // Extract MM-DD from YYYY-MM-DD
              }
            },
            rotate: this.currentDataType === 'hour' ? 0 : 0
          },
        },
        yAxis: {
          type: "value",
          min: yAxisMin,
          max: yAxisMax,
          splitLine: {
            show: true,
            lineStyle: {
              color: "rgba(31,99,163,.2)",
            },
          },
          axisLine: {
            lineStyle: {
              color: "rgba(31,99,163,.1)",
            },
          },
          axisLabel: {
            color: "#7EB7FD",
            fontWeight: "500",
            formatter: function(value) {
              if (value >= 10000) {
                return (value / 10000).toFixed(1) + '万';
              }
              return value;
            }
          },
        },
        tooltip: {
          trigger: "axis",
          backgroundColor: "rgba(0,0,0,.6)",
          borderColor: "rgba(147, 235, 248, .8)",
          textStyle: {
            color: "#FFF",
          },
          formatter: (params) => {
            const dataPoint = params[0];
            let timeFormat = dataPoint.name;
            
            // Format time display in tooltip
            if (this.currentDataType === 'hour') {
              // For hourly data, show "YYYY-MM-DD HH:MM"
              timeFormat = dataPoint.name;
            } else {
              // For daily data, show "YYYY-MM-DD"
              timeFormat = dataPoint.name;
            }
            
            let valueFormat = dataPoint.value.toLocaleString() + '人';
            if (dataPoint.value >= 10000) {
              valueFormat = (dataPoint.value / 10000).toFixed(2) + '万人';
            }
            
            return `${timeFormat}<br/>${dataPoint.seriesName}: ${valueFormat}`;
          }
        },
        grid: {
          show: true,
          left: "10px",
          right: "30px",
          bottom: "10px",
          top: "40px",
          containLabel: true,
          borderColor: "#1F63A3",
        },
        series: [
          {
            data: yData,
            type: "line",
            smooth: true,
            symbol: "circle",
            symbolSize: 6,
            name: this.currentDataType === 'hour' ? "小时客流量" : "日客流量",
            color: "rgba(9,202,243,.7)",
            areaStyle: {
              color: new graphic.LinearGradient(
                0,
                0,
                0,
                1,
                [
                  {
                    offset: 0,
                    color: "rgba(9,202,243,.7)",
                  },
                  {
                    offset: 1,
                    color: "rgba(9,202,243,.0)",
                  },
                ],
                false
              ),
            },
            markPoint: {
              data: [
                {
                  name: "最大值",
                  type: "max",
                  valueDim: "y",
                  symbol: "rect",
                  symbolSize: [80, 26],
                  symbolOffset: [0, -20],
                  itemStyle: {
                    color: "rgba(0,0,0,0)",
                  },
                  label: {
                    color: "#09CAF3",
                    backgroundColor: "rgba(9,202,243,0.1)",
                    borderRadius: 6,
                    padding: [7, 14],
                    borderWidth: 0.5,
                    borderColor: "rgba(9,202,243,.5)",
                    formatter: function(params) {
                      if (params.value >= 10000) {
                        return `最大值: ${(params.value / 10000).toFixed(1)}万人`;
                      }
                      return `最大值: ${params.value}人`;
                    }
                  },
                },
                {
                  name: "最大值",
                  type: "max",
                  valueDim: "y",
                  symbol: "circle",
                  symbolSize: 6,
                  itemStyle: {
                    color: "#09CAF3",
                    shadowColor: "#09CAF3",
                    shadowBlur: 8,
                  },
                  label: {
                    formatter: "",
                  },
                },
              ],
            },
          }
        ],
      };
    },
  },
};
</script>
<style lang='scss' scoped>
.visitor-flow-container {
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
  
  .right_top_inner {
    width: 100%;
    height: 100%;
  }
}
</style>