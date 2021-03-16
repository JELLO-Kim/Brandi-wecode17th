<template>
  <div>
    <info-text label="최신 등록 순으로 노출됩니다."/>
    <table class="bordered">
      <thead>
      <tr>
        <th>날짜</th>
        <th>주문상태</th>
      </tr>
      </thead>
      <tbody>
      <tr>
        <td>2020-10-29 15:48:47</td>
        <td>상품준비</td>
      </tr>
      <tr>
        <td>2020-10-29 15:48:47</td>
        <td>결제완료</td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import InfoText from '@/pages/Components/info-text'
export default {
  components: {
    InfoText
  },
  props: {
    dataStore: {
      default () {
        return {}
      }
    }
  },
  data () {
    return {
    }
  },
  computed: {
  },
  methods: {
  }
}
</script>
<style scoped>
.bordered {
  width: 100%;
}
</style>
