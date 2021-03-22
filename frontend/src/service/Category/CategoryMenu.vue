<template>
  <div class="body">
    <h2>Best</h2>
    <ul>
      <li v-for="item in menu" :key="item" :class="{'open': item.open}">
        <p @click="toggleOpen(item)">{{ item.label }}</p>
        <ul v-if="item.child">
          <li v-for="sub in item.child" :key="sub">{{ sub.label }}</li>
        </ul>
      </li>
    </ul>
  </div>
</template>
<script>

export default {
  name: 'CategoryMenu',
  components: {
  },
  data () {
    return {
      menu: [
        {
          label: '전체',
          child: [
            {
              label: '전체'
            }
          ]
        },
        {
          label: '쇼핑몰 · 마켓',
          child: [
            {
              label: '전체'
            },
            {
              label: '아웃터'
            },
            {
              label: '상의'
            },
            {
              label: '바지'
            },
            {
              label: '원피스'
            }
          ]
        }
      ]
    }
  },
  created () {
    this.menu.forEach(m => {
      this.$set(m, 'open', false)
    })
  },
  methods: {
    toggleOpen (item) {
      item.open = !item.open
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
