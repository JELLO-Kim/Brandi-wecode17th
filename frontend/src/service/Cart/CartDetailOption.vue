<template>
  <div>
    <tr class="cart-list-product">
      <td>
        <CheckBox class="checkItem" v-model="list.checked"></CheckBox>
      </td>
      <td>
        <img
          :src="this.list.imageUrl"
          alt=""
        />
      </td>
      <td>
        <div>{{ this.list.name }}</div>
        <div>{{ this.list.color }} / {{ this.list.size}} (일반배송)</div>
      </td>
      <td>
        <div>
          <button v-on:click="subItem">-</button>
          <input type="text" :value="this.list.quantity" >
          <button v-on:click="addItem">+</button>
        </div>
      </td>
      <td>
        <span>{{ this.list.price * this.list.quantity | makeComma }}원</span>
        <button @click="nowBuyItem">바로주문</button>
      </td>
    </tr>
  </div>
</template>

<script>
import CheckBox from '@/service/Components/CheckBox'
import { EventBus } from '@/service/util/event-bus'

export default {
  data () {
    return {
      isChecked: false
    }
  },
  props: {
    list: {
      type: Object,
      default () {
        return {
          id: Number,
          name: String,
          thumbnail: String,
          price: Number,
          color: String,
          size: String,
          quantity: Number,
          checked: Boolean
        }
      }
    }
  },
  components: {
    CheckBox
  },
  methods: {
    subItem () {
      if (this.list.quantity <= 1) return
      this.list.quantity = this.list.quantity - 1
      if (this.isChecked) {
        const totalPrice = -this.list.price
        EventBus.$emit('cal-price', totalPrice)
      }
    },
    addItem () {
      this.list.quantity = this.list.quantity + 1
      if (this.isChecked) {
        const totalPrice = +this.list.price
        EventBus.$emit('cal-price', totalPrice)
      }
    },
    checkItem () {
      if (this.isChecked) {
        const data = {
          id: this.list.id,
          quantity: this.list.quantity,
          color: this.list.color,
          size: this.list.size,
          price: this.list.price
        }

        EventBus.$emit('check-item', data)
      } else {
        EventBus.$emit('unCheck-item', {
          id: this.list.id
        })
      }
    },
    nowBuyItem () {
      const nowData = {
        totalPrice: this.list.price * this.list.quantity,
        items: {
          id: this.list.id,
          quantity: this.list.quantity,
          color: this.list.color,
          size: this.list.size,
          price: this.list.price
        }
      }
      localStorage.removeItem('cart')
      localStorage.setItem('cart', JSON.stringify(nowData))
      this.$router.push('/order')
    }
  }

}
</script>

<style lang="scss" scoped>
.cart-list-product {
  padding: 15px 0;

  td {
    padding: 15px 15px 15px 0;
  }
  td:nth-child(2) {
    width: 80px;
    height: 80px;
    overflow: hidden;

    img {
      width: 80px;
      height: auto;
    }
  }
  td:nth-child(3) {
    width: 60%;
    text-align: left;

    div:first-child {
      font-size: 17px;
    }
    div:last-child {
      color: rgb(135, 135, 135);
    }
  }
  td:nth-child(4) {
    div {
      text-align: center;

      button {
        background-color: white;
        border: solid 1px rgb(228, 228, 228);
        width: 25px;
      }
      input {
        width: 20px;
        padding: 4px 4px;
        border: 0;
        font-size: 10px;
      }
    }
  }
  td:nth-child(5) {
    display: flex;
    flex-direction: column;
    * {
      display: inline-block;
    }
    span {
      font-size: 23px;
      font-weight: 600;
    }
    button {
      font-size: 13px;
      margin: 0 auto;
      width: 120px;
      background-color: black;
      color: white;
      padding: 10px 20px;
    }
  }
}
</style>
