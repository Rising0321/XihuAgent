<!--
 * @Author: daidai
 * @Date: 2022-02-28 16:16:42
 * @LastEditors: Please set LastEditors
 * @LastEditTime: 2022-07-20 17:57:11
 * @FilePath: \web-pc\src\pages\big-screen\view\indexs\left-center.vue
-->
<template>
    <div class="water-quality-container">
        <ul class="water_quality flex" v-if="pageflag">
            <li class="water_quality-item" style="color: #00fdfa">
                <div class="water_quality_value allnum">
                    <dv-digital-flop :config="phConfig" style="width:100%;height:100%;" />
                </div>
                <p>PH值</p>
            </li>
            <li class="water_quality-item" style="color: #07f7a8">
                <div class="water_quality_value online">
                    <dv-digital-flop :config="dissolvedOxygenConfig" style="width:100%;height:100%;" />
                </div>
                <p>溶解氧 (mg/L)</p>
            </li>
            <li class="water_quality-item" style="color: #e3b337">
                <div class="water_quality_value offline">
                    <dv-digital-flop :config="totalPhosphorusConfig" style="width:100%;height:100%;" />
                </div>
                <p>总磷 (mg/L)</p>
            </li>
            <li class="water_quality-item" style="color: #f5023d">
                <div class="water_quality_value laramnum">
                    <dv-digital-flop :config="chlorophyllConfig" style="width:100%;height:100%;" />
                </div>
                <p>叶绿素 (μg/L)</p>
            </li>
        </ul>
        <ul class="water_quality flex mt-10" v-if="pageflag">
            <li class="water_quality-item" style="color: #00fdfa">
                <div class="water_quality_value allnum">
                    <dv-digital-flop :config="conductivityConfig" style="width:100%;height:100%;" />
                </div>
                <p>电导率 (mS/m)</p>
            </li>
            <li class="water_quality-item" style="color: #07f7a8">
                <div class="water_quality_value online">
                    <dv-digital-flop :config="turbidityConfig" style="width:100%;height:100%;" />
                </div>
                <p>浊度 (NTU)</p>
            </li>
            <li class="water_quality-item" style="color: #e3b337">
                <div class="water_quality_value offline">
                    <dv-digital-flop :config="temperatureConfig" style="width:100%;height:100%;" />
                </div>
                <p>水温 (°C)</p>
            </li>
        </ul>
        <Reacquire v-else @onclick="getData" line-height="200px">
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
            waterQualityData: {},
            pageflag: true,
            timer: null,
            phConfig: {
                number: [0],
                content: '{nt}',
                toFixed: 2,
                style: {
                    ...style,
                    fill: "#00fdfa",
                },
            },
            dissolvedOxygenConfig: {
                number: [0],
                content: '{nt}',
                toFixed: 2,
                style: {
                    ...style,
                    fill: "#07f7a8",
                },
            },
            totalPhosphorusConfig: {
                number: [0],
                content: '{nt}',
                toFixed: 2,
                style: {
                    ...style,
                    fill: "#e3b337",
                },
            },
            chlorophyllConfig: {
                number: [0],
                content: '{nt}',
                toFixed: 2,
                style: {
                    ...style,
                    fill: "#f5023d",
                },
            },
            conductivityConfig: {
                number: [0],
                content: '{nt}',
                toFixed: 2,
                style: {
                    ...style,
                    fill: "#00fdfa",
                },
            },
            turbidityConfig: {
                number: [0],
                content: '{nt}',
                toFixed: 2,
                style: {
                    ...style,
                    fill: "#07f7a8",
                },
            },
            temperatureConfig: {
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
    filters: {
        numsFilter(msg) {
            return msg || 0;
        },
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
            currentGET("water-quality").then((res) => {
                if (!this.timer) {
                    console.log("水质数据", res);
                }
                if (res.success) {
                    this.waterQualityData = res.data;
                    
                    // Update the digital flop values with 2 decimal places
                    this.phConfig = {
                        ...this.phConfig,
                        number: [parseFloat(res.data.PH)]
                    }
                    this.dissolvedOxygenConfig = {
                        ...this.dissolvedOxygenConfig,
                        number: [parseFloat(res.data['溶解氧 (mg/L)'])]
                    }
                    this.totalPhosphorusConfig = {
                        ...this.totalPhosphorusConfig,
                        number: [parseFloat(res.data['总磷 (mg/L)'])]
                    }
                    this.chlorophyllConfig = {
                        ...this.chlorophyllConfig,
                        number: [parseFloat(res.data['叶绿素 (μg/L)'])]
                    }
                    this.conductivityConfig = {
                        ...this.conductivityConfig,
                        number: [parseFloat(res.data['电导率 (mS/m)'])]
                    }
                    this.turbidityConfig = {
                        ...this.turbidityConfig,
                        number: [parseFloat(res.data['浊度 (NTU)'])]
                    }
                    this.temperatureConfig = {
                        ...this.temperatureConfig,
                        number: [parseFloat(res.data['水温 (°C)'])]
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
.water_quality {
    li {
        flex: 1;

        p {
            text-align: center;
            height: 16px;
            font-size: 16px;
        }

        .water_quality_value {
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