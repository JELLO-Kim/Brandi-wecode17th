<template>
<div>
  <a-button :type="allChecked ? 'primary':'normal'" @click="checkAll" :disabled="disabled">전체</a-button>
  <a-button class="sub-button" :type="value.includes(item.value) ? 'primary':'normal'" v-for="item in items" :key="item.value" @click="toggle(item)" :disabled="disabled">{{ item.label }}</a-button>
</div>
</template>

<script>
export default {
  name: 'multi-select-buttons',
  data () {
    return {
      allChecked: true
    }
  },
  props: {
    items: {
      default () {
        return []
      }
    },
    value: {
      default () {
        return []
      }
    },
    disabled: {
      default () {
        return false
      }
    },
    // 복수 선택 가능 여부
    multipleSelect: {
      default () {
        return true
      }
    }
  },
  computed: {
    allCheckedComputed () {
      return this.items.length === this.value.length
    }
  },
  mounted () {
    // 전체 선택이 아닌 경우 발라냄 (한건도 선택된게 아닌데, 모든 버튼을 선택한것도 아니면)
    if (this.value.length !== 0 && this.items.length !== this.value.length) {
      this.allChecked = false
    }
  },
  methods: {
    checkAll () {
      this.allChecked = true
      this.$emit('input', [])
    },
    toggle (item) {
      if (this.multipleSelect) {
        const newValue = [...this.value]
        const index = newValue.indexOf(item.value)
        if (index >= 0) {
          newValue.splice(index, 1)
        } else {
          newValue.push(item.value)
          this.allChecked = false
        }
        this.$emit('input', newValue)
      } else {
        // 단일 선택
        this.allChecked = false
        this.$emit('input', [item.value])
      }
    }
  },
  watch: {
    allCheckedComputed (v) {
      if (v) {
        this.checkAll()
      }
    },
    value (v) {
      if (v.length === 0) {
        this.allChecked = true
      } else {
        // 전체 선택이 아닌 경우 발라냄 (한건도 선택된게 아닌데, 모든 버튼을 선택한것도 아니면)
        if (this.value.length !== 0 && this.items.length !== this.value.length) {
          this.allChecked = false
        }
      }
    }
  }
}
</script>

<style scoped>
.sub-button {
  margin: 0 2px;
}
</style>
