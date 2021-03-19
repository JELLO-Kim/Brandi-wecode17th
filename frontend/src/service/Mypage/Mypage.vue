<template>
  <div>
    <div class="myPage">마이페이지</div>
    <div class="wrap">
      <div class="menuContainer">
        <div
          :class="[
            getCurrentPage() === 'orderList' ? 'active' : 'deactive',
            'menu',
          ]"
          @click="linkToPage"
        >
          <div class="imgContainer">
            <img src="/Images/ic-mypage-orderlist-s@3x.png" alt="orderList" name="orderList" />
          </div>
          <div class="menuText">
            <div :class="['text', 'orderList']">주문/배송조회</div>
            <img src="/Images/ic-titleic-detailpage-moreaction@3x.png" alt=">" name="orderList" />
          </div>
        </div>

        <div class="divider"></div>
        <div
          :class="[
            getCurrentPage() === 'point' ? 'active' : 'deactive',
            'menu',
          ]"
          @click="linkToPage"
        >
          <div class="imgContainer">
            <img src="/Images/ic-my-point-s@3x.png" alt="point" name="point" />
          </div>
          <div class="menuText">
            <span :class="['text', 'point']">포인트</span>
            <span class="number">{{ point }}</span>
            <img src="/Images/ic-titleic-detailpage-moreaction@3x.png" alt=">" name="point" />
          </div>
        </div>
        <div class="divider"></div>
        <div
          :class="[
            getCurrentPage() === 'coupon' ? 'active' : 'deactive',
            'menu',
          ]"
          @click="linkToPage"
        >
          <div class="imgContainer">
            <img src="/Images/ic-mypage-coupon-s@3x.png" alt="coupon" name="coupon" />
          </div>
          <div class="menuText">
            <span :class="['text', 'coupon']">쿠폰</span>
            <span class="number">{{ coupon }}</span>
            <img src="/Images/ic-titleic-detailpage-moreaction@3x.png" alt=">" name="coupon" />
          </div>
        </div>
        <div class="divider"></div>
        <div
          :class="[
            getCurrentPage() === 'qna' ? 'active' : 'deactive',
            'menu',
          ]"
          @click="linkToPage"
        >
          <div class="imgContainer">
            <img src="/Images/ic-mypage-qna-s@3x.png" alt="qna" name="qna"/>
          </div>
          <div class="menuText">
            <span class="text">Q & A</span>
            <img src="/Images/ic-titleic-detailpage-moreaction@3x.png" alt=">" name="qna"/>
          </div>
        </div>
        <div class="divider"></div>
        <div :class="[getCurrentPage() === 'faq' ? 'active' : 'deactive', 'menu']">
          <div class="imgContainer">
            <img src="/Images/ic-myshopping-faq-s@3x.png" alt="faq" />
          </div>
          <div class="menuText">
            <span class="text">FAQ</span>
            <img src="/Images/ic-titleic-detailpage-moreaction@3x.png" alt=">" />
          </div>
        </div>
      </div>
    </div>
    <router-view class="router"></router-view>
  </div>
</template>

<script>
export default {
  data () {
    return {
      currentPage: '',
      point: 0,
      coupon: 0
    }
  },
  methods: {
    getCurrentPage () {
      const currentUrl = this.$router.currentRoute.path

      if (currentUrl === '/mypage/point') {
        this.currentPage = 'point'
      } else if (currentUrl === '/mypage/coupon') {
        this.currentPage = 'coupon'
      } else if (currentUrl === '/mypage/qna') {
        this.currentPage = 'qna'
      } else if (currentUrl === '/mypage/faq') {
        this.currentPage = 'faq'
      } else if (currentUrl === '/mypage/orderList') {
        this.currentPage = 'orderList'
      }
      return this.currentPage
    },

    linkToPage (event) {
      let linkPage = ''
      if (event.target.name) {
        linkPage = event.target.name
      } else {
        linkPage = event.target.className.split(' ')[1]
      }

      if (this.$router.currentRoute.path.split('/')[2] !== linkPage) {
        this.$router.push(`${linkPage}`)
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.myPage {
  text-align: center;
  margin: 80px 0 50px 0;
  font-size: 28px;
  font-weight: 500;
}

.wrap {
  display: flex;
  justify-content: center;
  margin-bottom: 100px;

  .menuContainer {
    border: 1px solid black;
    display: flex;
    justify-content: space-between;
    padding: 60px 0;
    max-width: 1260px;

    .active {
      font-weight: bold;
    }

    .deactive {
      img {
        opacity: 0.4;
      }

      .text {
        opacity: 0.4;
      }
    }

    .menu {
      text-align: center;
      margin: 0 80px;
      cursor: pointer;

      .imgContainer {
        img {
          width: 70px;
        }
      }

      .menuText {
        div {
          display: inline;
        }

        img {
          width: 8px;
        }

        .number {
          opacity: 1;
          color: red;
          font-weight: bold;
        }
      }
    }
    .divider {
      background-color: black;
      width: 0.5px;
    }
  }
}

.router {
  display: flex;
  justify-content: center;
  margin-bottom: 50px;
}
</style>
