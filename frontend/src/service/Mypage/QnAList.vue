<template>
    <QnA v-bind:title="title" v-bind:isMypage="isMypage"></QnA>
</template>

<script>
// import Pagenation from '@/service/Components/Pagenation'
import QnA from '@/service/Detail/QnA'

export default {
  created () {
  },
  data () {
    return {
      isMypage: true,
      title: '상품 Q&A'
    }
  },
  components: {
    // Pagenation
    QnA
  },
  methods: {
    togleAnswer (answer) {
      answer.answerShow = !answer.answerShow
    }
  }
}
</script>

<style lang="scss" scoped>
</style>
