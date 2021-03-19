<template>
  <div>
    <label>
      <CheckBox v-model="testCheck"></CheckBox>
      111
    </label>
  </div>
</template>

<script>
import CheckBox from '@/service/Components/CheckBox'

export default {
  name: 'CategoryMain',
  data () {
    return {
      testCheck: false
    }
  },
  components: {
    CheckBox
  }
}
</script>

<style lang="scss" scoped>

</style>
