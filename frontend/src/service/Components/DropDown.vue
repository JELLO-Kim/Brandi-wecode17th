<template>
  <div class="container">
    <div class="selctbox" @click.prevent.stop="toggleItem">{{displayLabelName}}</div>
    <div class="itembox" v-show="isOpen">
      <div class="item" @click="selectItem(null)">
        {{placeholder}}
      </div>
      <div
        v-for="item in items"
        class="item"
        v-bind:key="item.key"
        @click="selectItem(item)"
      >
        {{ item.label }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DropDown',
  data () {
    return {
      isOpen: false
    }
  },
  props: {
    value: String,
    items: {
      type: Array,
      default () {
        return [
          {
            key: '',
            label: ''
          }
        ]
      }
    },
    placeholder: {
      type: String,
      default () {
        return '선택해주세요'
      }
    }
  },
  beforeMount () {
    document.body.addEventListener('click', this.clickout)
  },
  beforeDestroy () {
    document.body.removeEventListener('click', this.clickout)
  },
  computed: {
    displayLabelName () {
      if (this.selectedItem) {
        return this.selectedItem.label
      }
      return this.placeholder
    },
    selectedItem () {
      return this.items.find(d => d.key === this.value)
    }
  },
  methods: {
    toggleItem () {
      this.isOpen = !this.isOpen
    },
    selectItem (item) {
      this.isOpen = false
      if (item === null) {
        this.$emit('input', null)
        this.$emit('change', null)
      } else {
        this.$emit('input', item.key)
        this.$emit('change', item.key)
      }
    },
    clickout () {
      this.isOpen = false
    }
  },
  watch: {
  }
}
</script>

<style lang="scss" scoped>
.container {
  display: inline-block;
  position: relative;
  width: 100%;
  .selctbox {
    position: relative;
    width: 100%;
    padding: 13px 10px 13px 10px;
    background-color: white;
    border: 1px solid #e1e1e1;
    font-size: 13px;
    color: #666;
    cursor: pointer;
    &::after {
      content: "";
      display: block;
      position: absolute;
      right: 10px;
      top: 15px;
      width: 20px;
      height: 20px;
      background: #FFF url(/images/ic-arrow-bl-down@3x.png) no-repeat 50% 50%;
      background-size: 20px;
    }
  }
  .itembox {
    position: absolute;
    z-index: 1;
    width: 100%;
    // padding: 13px 10px 13px 10px;
    background-color: white;
    border: 1px solid #e1e1e1;
    font-size: 13px;
    .item {
      padding: 13px 10px 13px 10px;
      color: #666;
      cursor: pointer;
      &:hover {
        background: #f6f6f6;
      }
    }
  }
}
</style>
