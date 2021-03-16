<template>
  <div>
    <a-row :gutter="16">
      <a-col :lg="8" :xs="24">
        <a-card class="box" :loading="dataStore.loading">
          <a-row class="row">
            <a-col :span="12" >상품 준비</a-col>
            <a-col :span="12" class="text-right">{{dataStore.dashboardData.prepare_count}} 건</a-col>
          </a-row>
<!--          <a-row>-->
<!--            <a-col :span="12">배송 준비</a-col>-->
<!--            <a-col :span="12" class="text-right">1 건</a-col>-->
<!--          </a-row>-->
          <a-row class="row">
            <a-col :span="12">배송 중</a-col>
            <a-col :span="12" class="text-right">0 건</a-col>
          </a-row>
          <a-row class="row">
            <a-col :span="12">배송 완료</a-col>
            <a-col :span="12" class="text-right">{{dataStore.dashboardData.complete_count}} 건</a-col>
          </a-row>
          <a-row>
            <a-col :span="12">구매 확정</a-col>
            <a-col :span="12" class="text-right">0 건</a-col>
          </a-row>
        </a-card>
      </a-col>
      <a-col :lg="8" :xs="24">
        <a-card class="box" :loading="dataStore.loading">
          <a-row class="row">
            <a-col :span="12">환불 요청</a-col>
            <a-col :span="12" class="text-right">0 건</a-col>
          </a-row>
          <a-row class="row">
            <a-col :span="12">반품 진행</a-col>
            <a-col :span="12" class="text-right">0 건</a-col>
          </a-row>
          <a-row class="row">
            <a-col :span="12">주문 취소중</a-col>
            <a-col :span="12" class="text-right">0 건</a-col>
          </a-row>
          <a-row class="row">
            <a-col :span="12">환불 승인중</a-col>
            <a-col :span="12" class="text-right">0 건</a-col>
          </a-row>
        </a-card>
      </a-col>

      <a-col :lg="8" :xs="24">
        <a-card class="box" :loading="dataStore.loading">
          <a-row class="row">
            <a-col :span="12">즐겨찾기 수</a-col>
            <a-col :span="12" class="text-right">0 개</a-col>
          </a-row>
          <a-row class="row">
            <a-col :span="12">전체 상품 수</a-col>
            <a-col :span="12" class="text-right">{{dataStore.dashboardData.total_count}} 개</a-col>
          </a-row>
          <a-row class="row">
            <a-col :span="12">노출 상품 수</a-col>
            <a-col :span="12" class="text-right">{{dataStore.dashboardData.display_count}} 개</a-col>
          </a-row>
          <a-row class="row">
            <a-col :span="12">API연동 상품 수</a-col>
            <a-col :span="12" class="text-right">0 개</a-col>
          </a-row>
        </a-card>
      </a-col>
    </a-row>

    <a-row :gutter="16" class="chart-row">
      <a-col :lg="12" :xs="24">
        <a-card title="매출 통계 [최근 30일간의 결제완료된 주문 건수의 합계]" size="small" class="chart" :loading="dataStore.loading">
          <line-chart :chart-data="chartData1" :options="chartOptions" :style="{height: '270px', position: 'relative'}"></line-chart>
        </a-card>
      </a-col>
      <a-col :lg="12" :xs="24">
        <a-card title=" 매출 통계 [최근 30일간의 결제완료된 주문 금액의 합계]" size="small" class="chart" :loading="dataStore.loading">
          <line-chart :chart-data="chartData2" :options="chartOptions" :style="{height: '270px', position: 'relative'}"></line-chart>
        </a-card>
      </a-col>
    </a-row>

  </div>
</template>

<script>
import LineChart from './line-chart'
import moment from 'moment'
import store from './dashboard-store'
import Vue from 'vue'

export default {
  components: {
    LineChart
  },
  created () {
    let val1 = Math.floor(Math.random() * 1000) + 50
    let val2 = Math.floor(Math.random() * 1000) + 50
    for (let i = 0; i < 30; i++) {
      const date = moment('2020-10-01').add(i, 'days').format('YYYY-MM-DD')
      this.chartData1.labels.push(date)
      this.chartData2.labels.push(date)
      val1 += Math.floor(Math.random() * 200) - 100
      val2 += Math.floor(Math.random() * 200) - 100
      if (val1 < 0) val1 = 0
      if (val2 < 0) val2 = 0
      this.chartData1.datasets[0].data.push(val1)
      this.chartData2.datasets[0].data.push(val2)
    }
  },
  data () {
    return {
      dataStore: new Vue(store),
      chartData1: {
        labels: [],
        datasets: [
          {
            label: '결제 건수',
            backgroundColor: 'rgba(255,60,60,0.3)',
            borderColor: '#d97070',
            borderWidth: 2,
            data: [
            ]
          }
        ]
      },
      chartData2: {
        labels: [],
        datasets: [
          {
            label: '결제 건수',
            backgroundColor: 'rgb(60,154,255, 0.3)',
            borderColor: '#70a8d9',
            borderWidth: 2,
            data: [
            ]
          }
        ]
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        elements: {
          line: {
            tension: 0
          }
        },
        legend: {
          display: false
        },
        scales: {
          xAxes: [{
            type: 'time',
            time: {
              displayFormats: {
                day: 'YY-MM-DD'
              }
            }
          }]
        }
      }
    }
  }

}
</script>

<style scoped>
.row {
  margin: 5px 0;
}
.text-right {
  font-weight: bold;
  text-align: right;
}
.box {
  height: 150px;
}
.chart {
  height: 350px;
}
.chart-row {
  margin-top: 15px;
}
</style>
