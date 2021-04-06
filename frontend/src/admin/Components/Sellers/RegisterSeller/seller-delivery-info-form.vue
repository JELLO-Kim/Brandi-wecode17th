<template>
  <div>
    <a-descriptions bordered size="small" class="seller-from" label-width="20%">
      <a-descriptions-item :span="3">
        <template slot="label">배송 정보 <span class="required">*</span></template>
        <a-textarea rows="5" v-model="dataStore.detailData.deliveryInfo" placeholder="ex)
도서산간 지역은 배송비가 추가비용이 발생할 수 있습니다.
결제 완료 후 1~3일 후 출고됩니다."></a-textarea>
      </a-descriptions-item>
      <a-descriptions-item :span="3">
        <template slot="label">교환/환불 정보 <span class="required">*</span></template>
        <a-textarea rows="5" v-model="dataStore.detailData.refundInfo" placeholder="ex)
브랜디는 소비자보호법 및 전자상거래법을 기반한 환불보장제를 운영 중에 있습니다.
정당하지 않은 사유로 인한 환불 거부 등은 제재 사유가 될 수 있는 점 참고 부탁드립니다."></a-textarea>
      </a-descriptions-item>

    </a-descriptions>
  </div>
</template>

<script>
export default {
  data () {
    return {
      sellerType: 1
    }
  },
  props: {
    dataStore: {
      default () {
        return {}
      }
    }
  }
}
</script>

<style type="scss" scoped>
.normal-size {
  width: 200px;
}
.required {
  color: red
}
</style>
