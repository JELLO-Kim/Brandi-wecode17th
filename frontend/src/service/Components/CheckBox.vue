<template>
  <div>
    <input type="checkbox" v-model="checked" @change="change">
    <span :style="{backgroundPosition: checked ? '0 -17px': '0 0'}" @click.prevent="click"></span>
  </div>
</template>

<script>
export default {
  name: 'CheckBox',
  props: {
    value: Boolean
  },
  data () {
    return {
      checked: false
    }
  },
  methods: {
    click () {
      this.checked = !this.checked
      this.$emit('input', this.checked)
      this.$emit('change', this.checked)
    },
    change () {
      this.$emit('input', this.checked)
      this.$emit('change', this.checked)
    }
  },
  watch: {
    value (v) {
      this.checked = v
    }
  }
}
</script>

<style lang="scss" scoped>
div {
  position: relative;
  display: inline-block;
  vertical-align: middle;
  top: 3px;
  margin-right: 10px;
}
input {
  position: relative;
  top: -4px;
  left: 2px;
}
span {
  display: inline-block;
  position: absolute;
  left: 0;
  top: 0;
  width: 17px;
  height: 17px;
  background: url(/images/icon_check_bg.png) no-repeat 0 0;
}
</style>
