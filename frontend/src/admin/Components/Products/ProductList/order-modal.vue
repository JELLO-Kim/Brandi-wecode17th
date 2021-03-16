<template>
  <a-modal v-model="visible" :closable="false" :maskClosable="false" @onOk="save" @onCancel="close">
    <h4>주문하기</h4>
    <div>
      productItem: {{productItem}}
      구현 하세요<br>
      구현 하세요
    </div>
  </a-modal>
</template>

<script>

export default {
  name: 'order-modal',
  data () {
    return {
      productItem: {},
      visible: false
    }
  },
  mounted () {
  },
  methods: {
    // 저장하기
    save () {
      console.log('save')
    },
    show (productItem) {
      this.productItem = productItem
      this.visible = true
    },
    close () {
      this.visible = false
      console.log('close')
    }
  },
  computed: {
  }
}
</script>
<style scoped>
</style>
