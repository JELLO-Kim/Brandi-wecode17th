<template>
  <div>
    <table class="bordered">
      <thead>
      <tr>
        <th>날짜</th>
        <th>주문상태</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="item in dataStore.detailData.order_histories" :key="item">
        <td>{{ item.update_time }}</td>
        <td>{{ item.order_status_id | typeToName('orderStatusTypes') }}</td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import CommonMixin from '@/admin/mixins/common-mixin'
export default {
  name: 'order-history-info-form',
  mixins: [CommonMixin],
  components: {
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
