<template>
<div class="container">
  <div class="selectTitle">
    <p>{{ item.colorName }} / {{ item.sizeName }}</p>
    <div @click="remove" class="removeBtn">
      <img
        src="/images/img_icon_x.png"
      />
    </div>
  </div>
  <div class="selectPrice">
    <div class="selectQuantity">
      <button
        class="quantityControlBtn"
        name="minus"
        @click="subQuantity"
      >
        -
      </button>
      <input class="productQuantity" v-model="item.quantity" readonly />
      <button
        class="quantityControlBtn"
        name="plus"
        @click="addQuantity"
      >
        +
      </button>
    </div>
    <p>
      {{
        item.price * item.quantity | makeComma
      }}원
    </p>
  </div>
</div>
</template>

<script>
export default {
  name: 'OptionQuantity',
  props: {
    item: {
      type: Object,
      default () {
        return {
          quantity: 1,
          color: 'color',
          size: 'size',
          price: 1000
        }
      }
    }
  },
  methods: {
    subQuantity () {
      if (this.item.quantity > 1) {
        this.item.quantity--
      }
    },
    addQuantity () {
      if (this.item.quantity < 20) {
        this.item.quantity++
      }
    },
    remove () {
      this.$emit('remove', this.item)
    }
  }
}
</script>

<style lang="scss" scoped>
.container {
  padding: 15px;
  background: #fafafa;
  border: 1px solid #f1f1f1;
  .removeBtn {
    cursor: pointer;
  }
  .selectTitle {
    display: flex;
    justify-content: space-between;
  }
  .selectPrice {
    display: flex;
    justify-content: space-between;
    justify-items: center;
    overflow: hidden;
    p {
      margin: 0;
    }
    .selectQuantity {
      height: 28px;
      border: 1px solid #cdcdcd;

      .border {
        height: 100%;
        border: 1px solid #cdcdcd;
        background-color: #cdcdcd;
      }

      .quantityControlBtn {
        width: 28px;
        height: 28px;
        border: none;
        border-radius: 0;
        background: #00ff0000;
        font-size: 15px;
        color: #5d5d5d;
        outline: none;
        cursor: pointer;
        vertical-align: top;
        margin: 0;
        padding: 0;

        &:first-child {
          border-right: 2px solid #cdcdcd;
        }

        &:last-child {
          border-left: 2px solid #cdcdcd;
        }
      }

      .productQuantity {
        width: 35px;
        height: 28px;
        border: none;
        background-color: #00ff0000;
        border-width: 1px 0;
        font-size: 13px;
        color: #666;
        text-align: center;
        margin: 0;
        padding: 0;
        outline: none;
      }
    }
  }
}

</style>
