<template>
  <div class="body">
    <h2>Best</h2>
    <ul>
      <li v-for="item in menu" :key="item.id" :class="{'open': item.open}">
        <p @click="toggleOpen(item)">{{ item.name }}</p>
        <ul v-if="item.subCategory">
          <li v-for="sub in item.subCategory" :key="sub.id" :value="sub.id" @click="selectSub">{{ sub.name }}</li>
        </ul>
      </li>
    </ul>
  </div>
</template>

<script>
// import SERVER from '@/config'
// import API from '@/service/util/service-api'
import { EventBus } from '@/service/util/event-bus'

export default {
  name: 'CategoryMenu',
  created () {
    // API.methods
    //   .get(`${SERVER.SERVER}/products/category`)
    //   .then(res => {
    //     // console.log(res.data.result.data)
    //     this.menu = res.data.result.data

    //     this.menu.forEach(m => {
    //       this.$set(m, 'open', false)
    //     })
    //   })
    //   .catch(error => {
    //     alert(error.message)
    //   })
    this.menu.forEach(m => {
      this.$set(m, 'open', false)
    })
  },
  components: {
  },
  data () {
    return {
      menu: [
        {
          name: '전체',
          subCategory: [
            {
              id: 1,
              name: '전체'
            }
          ]
        },
        {
          name: '쇼핑몰 · 마켓',
          subCategory: [
            {
              id: 2,
              name: '전체'
            },
            {
              id: 3,
              name: '아웃터'
            },
            {
              id: 4,
              name: '상의'
            },
            {
              id: 5,
              name: '바지'
            },
            {
              id: 6,
              name: '원피스'
            }
          ]
        }
      ]
    }
  },
  methods: {
    toggleOpen (item) {
      item.open = !item.open
    },
    selectSub (e) {
      // console.log(e.target.value)
      EventBus.$emit('select-sub', e.target.value)
    }
  }
}
</script>

<style lang="scss" scoped>
.body {
    // &.open::after {
    //   transform: scaleY(-1);
    // }

  ul, li {
    margin: 0;
    padding: 0;
    list-style: none;
  }
  ul {
    border-top: 1px solid rgb(231, 231, 231);
    overflow: hidden;
  }
  li {
    padding: 0 0;
    border-bottom: 1px solid rgb(231, 231, 231);
    font-size: 16px;
    font-weight: 500;
    &.open p::after{
      transform: scaleY(-1);
    }
    &.open ul {
      height: 0;
    }
    p {
      position: relative;
      padding: 20px 0;
      margin: 0;
      cursor: pointer;
      &::after{
        content: "";
        display: block;
        position: absolute;
        right: 10px;
        top: 50%;
        width: 13px;
        height: 13px;
        margin-top: -8px;
        background: #FFF url(/images/ic-arrow-bl-down@3x.png) no-repeat 50% 50%;
        background-size: 13px;
        transition-duration: 0.2s;
      }
      &:hover {
        // background: #fafafa;
      }
    }
    // height: 60px;
    li {
      padding: 15px 10px;
      border-bottom: none;
      font-size: 14px;
      font-weight: 400;
      cursor: pointer;
      &:hover {
        background: #fafafa;
      }
    }
  }
}

</style>
