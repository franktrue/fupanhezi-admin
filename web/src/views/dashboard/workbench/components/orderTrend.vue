<template>
  <el-card
    class="card-view"
    :style="{
      backgroundColor: randomColor(),
    }"
  >
    <div id="orderTrend" :style="{width: pxData.wpx+'px',height: pxData.hpx+'px'}"></div>
  </el-card>
</template>

<script>
import { request } from '@/api/service'

export default {
  sort: 2,
  title: '订单金额趋势',
  name: 'orderTrend',
  icon: 'el-icon-s-data',
  description: '订单金额',
  height: 28,
  width: 20,
  isResizable: true,
  props: {
    pxData: {
      type: Object,
      require: false,
      default: () => ({
        wpx: 0,
        hpx: 0
      })
    }
  },
  watch: {
    pxData: {
      handler () {
        // eslint-disable-next-line no-unused-expressions
        this.myChart?.resize({ width: this.pxData.wpx, height: this.pxData.hpx })
      },
      immediate: true,
      deep: true
    }
  },
  data () {
    this.myChart = null
    return {
      data: []
    }
  },
  methods: {
    initGet () {
      request({
        url: '/api/order/datav/order_trend/'
      }).then((res) => {
        this.data = res.data.order_list
        this.drawLine()
      })
    },
    // 生成一个随机整数
    randomColor () {
      const color = ['#fffff']
      const ran = Math.floor(Math.random() * 4)
      return color[ran]
    },
    drawLine () {
      // 基于准备好的dom，初始化echarts实例
      // 绘制图表
      const xAxisData = this.data.map(item => item.day)
      const seriesData = this.data.map(item => item.amount)
      const seriesData2 = this.data.map(item => item.pay_count)
      const option = {
        tooltip: {
          trigger: 'axis',
          backgroundColor: 'rgba(255, 255, 255, 0.8)',
          textStyle: {
            color: '#666'
          },
          axisPointer: {
            lineStyle: {
              color: '#999',
              type: 'dotted',
              width: 1
            }
          }
        },
        legend: {
          data: ['订单金额', '成交笔数'],
          textStyle: {
            color: '#666',
            fontSize: 12
          }
        },
        grid: {
          top: 40,
          left: 80,
          right: 80,
          bottom: 60
        },
        xAxis: {
          data: xAxisData,
          boundaryGap: false,
          axisLine: {
            lineStyle: {
              color: '#aaa',
              width: 1
            }
          },
          axisLabel: {
            interval: 'auto',
            maxInterval: 1,
            rotate: 0,
            textStyle: {
              color: '#333',
              fontSize: 12
            }
          }
        },
        yAxis: [
          {
            type: 'value',
            name: '订单金额',
            position: 'left',
            axisLabel: {
              formatter: '{value} 元'
            }
          },
          {
            type: 'value',
            name: '成交笔数',
            position: 'right',
            interval: 1, //设置y轴刻度间隔
            axisLabel: {
              formatter: '{value} 笔'
            }
          }
        ],
        series: [
          {
            name: '订单金额',
            type: 'line',
            // yAxisIndex: 0,
            data: seriesData,
            symbol: 'circle',
            symbolSize: 6,
            smooth: true,
            tooltip: {
              valueFormatter: function (value) {
                return value.toFixed(2) + '元';
              }
            },
            lineStyle: {
              color: 'rgba(38,204,164, 0.8)',
              width: 2
            },
            itemStyle: {
              color: 'rgba(98,206,178, 0.8)',
              borderColor: 'rgba(38,204,164, 1)',
              borderWidth: 1
            },
            areaStyle: {
              color: {
                type: 'linear',
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [
                  {
                    offset: 0,
                    color: 'rgba(140,189,250, 0.8)'
                  },
                  {
                    offset: 1,
                    color: 'rgba(0, 128, 255, 0)'
                  }
                ]
              }
            }
          },
          {
            name: '成交笔数',
            type: 'line',
            yAxisIndex: 1,
            data: seriesData2,
            symbol: 'circle',
            smooth: true,
            symbolSize: 6,
            tooltip: {
              valueFormatter: function (value) {
                return value + '笔';
              }
            },
            lineStyle: {
              color: 'rgba(0,90,164, 0.8)',
              width: 2
            },
            itemStyle: {
              color: 'rgba(30,206,178, 0.8)',
              borderColor: 'rgba(0,90,,164, 1)',
              borderWidth: 1
            },
            areaStyle: {
              color: {
                type: 'linear',
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [
                  {
                    offset: 0,
                    color: 'rgba(0,100,250, 0.8)'
                  },
                  {
                    offset: 1,
                    color: 'rgba(0, 128, 255, 0)'
                  }
                ]
              }
            }
          }
        ]
      }
      this.myChart.setOption(option)
    }
  },
  mounted () {
    this.myChart = this.$echarts.init(document.getElementById('orderTrend'))
    this.initGet()
    this.drawLine()
  }
}
</script>

<style scoped lang="scss">
.card-view {
  //border-radius: 10px;
  color: $color-primary;
}

.el-card {
  height: 100%;
}
</style>
