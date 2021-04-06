<template>
  <a-modal v-model="visible" width="900" title="상품 수정 이력" @ok="handleOk" :cancelButtonProps="{style: { display: 'none' }}">
    <table class="bordered">
      <thead>
      <tr>
        <th>수정 날짜</th>
        <th>판매여부</th>
        <th>진열여부</th>
        <th>판매가격</th>
        <th>할인가격</th>
        <th>할인율</th>
        <th>수정자</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="item in mockup" :key="item">
        <td>{{ item.create_at }}</td>
        <td>{{ item.sale_yn }}</td>
        <td>{{ item.exhbit_yn }}</td>
        <td>{{ item.price }}</td>
        <td>{{ item.discout_price }}</td>
        <td>{{ item.rate }}</td>
        <td>{{ item.account }}</td>
      </tr>
      </tbody>
    </table>
  </a-modal>
</template>

<script>
export default {
  name: 'product-history-modal',
  props: {
    dataStore: {
      default () {
        return {}
      }
    }
  },
  data () {
    return {
      visible: false,
      mockup: [
      ]
    }
  },
  created () {
    for (let i = 0; i < 10; i++) {
      this.mockup.push({
        no: i,
        create_at: '2020-10-28 14:01:38',
        sale_yn: 'Y',
        exhbit_yn: 'Y',
        price: 44400,
        discout_price: 44400,
        rate: 0,
        account: 'intern_master(인턴 마스터 계정)'
      })
    }
  },
  methods: {
    handleOk () {
      this.hide()
    },
    show () {
      this.visible = true
    },
    hide () {
      this.visible = false
    }
  }
}
</script>

<style scoped>
table {
  width: 100%;
}
</style>
