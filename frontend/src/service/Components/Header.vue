<template>
  <div>
    <header class="mainHeader">
      <div class="headerBanner">
        <img
          class="bannerImg"
          src="https://image.brandi.me/home/banner/bannerImage_173997_1596420402.jpg"
          alt="jpg"
        />
      </div>
      <div class="searchContainer">
        <div class="searchBar">
          <h1 class="mainLogo" @click="linkToMain">
            <img class="logoImg" src="/Images/brandi-logo.png" alt="BRANDI" />
          </h1>
          <div>
            <form class="searchForm" action="/search">
              <button class="searchBtn"></button>
              <input class="searchInput" type="text" />
            </form>
          </div>
          <div class="searchNav">
            <span>찜</span>
            <div class="divider"></div>
            <span>장바구니</span>
            <div class="divider"></div>
            <span @click="linkToMyPage">마이페이지</span>
            <div class="divider"></div>
            <span @click="linkToLogin">
              {{
              getToken ? "로그아웃" : "로그인"
              }}
            </span>

            <div class="divider"></div>
            <span>입점문의</span>
          </div>
        </div>
      </div>
      <nav class="navBarContainer">
        <div class="navBar">
          <div class="selected"><a href="#">홈</a></div>
          <div><a href="#">하루배송</a></div>
          <div><a href="#" @click.prevent="linkToEvent">해택존</a></div>
          <div><a href="#">베스트</a></div>
          <div><a href="#">신상</a></div>
          <div><a href="#">특가</a></div>
          <div><a href="#">쇼핑몰 • 마켓</a></div>
          <div><a href="#">브랜드</a></div>
          <div><a href="#">뷰티</a></div>
          <div><a href="#">스토어</a></div>
        </div>
      </nav>
    </header>
  </div>
</template>

<script>
import { mapMutations, mapGetters } from 'vuex'

const serviceStore = 'serviceStore'

export default {
  methods: {
    ...mapMutations(serviceStore, ['getStorageToken']),

    linkToMain () {
      this.$route.path !== '/main'
        ? this.$router.push('/main')
        : this.$router.go('/main')
    },
    linkToLogin () {
      if (this.getToken) {
        localStorage.removeItem('user_id')
        localStorage.removeItem('access_token')
        localStorage.removeItem('user_email')
        this.getStorageToken()
        this.$route.path !== '/main' && this.$router.push('/main')
      } else {
        this.$route.path !== '/login' && this.$router.push('/login')
      }
    },
    linkToMyPage () {
      if (this.getToken) {
        this.$route.path !== '/mypage/orderList' &&
          this.$router.push('/mypage')
      } else {
        if (this.$route.path !== '/login') {
          this.$router.push('/login')
        }
      }
    },
    linkToEvent () {
      this.$router.push('/event')
    }
  },
  computed: {
    ...mapGetters(serviceStore, ['getToken'])
  }
}
</script>

<style lang="scss" scoped>
.mainHeader {
  .headerBanner {
    cursor: pointer;

    .bannerImg {
      width: 100%;
    }
  }

  .searchContainer {
    // position: sticky;
    // top: 0;

    background: #FFF;
    max-width: 1300px;
    margin: 0 auto;
    padding: 0 20px;

    .searchBar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      height: 120px;

      .mainLogo {
        display: flex;
        align-items: center;
        cursor: pointer;
        width: 190px;
        height: 80px;

        .logoImg {
          width: 150px;
        }
      }

      .searchForm {
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #eee;
        width: 505px;
        height: 40px;
        border-radius: 20px;

        .searchBtn {
          background: url(/Images/search-icon.png) no-repeat center;
          background-size: 22px;
          border: none;
          width: 30px;
          height: 30px;
        }

        .searchInput {
          background-color: #eee;
          border: none;
          width: 446px;
          height: 25px;
          font-size: 14px;
          line-height: 20px;
          margin-left: 10px;

          &:focus {
            outline: none;
          }
        }
      }

      .searchNav {
        display: flex;
        justify-content: center;
        cursor: pointer;
        font-size: 14px;

        .divider {
          background-color: gray;
          margin: 0 7px;
          width: 2px;
        }
      }
    }
  }

  .navBarContainer {
    border-top: 1px solid rgb(238, 238, 238);
    border-bottom: 1px solid rgb(238, 238, 238);
    .navBar {
      display: flex;
      justify-content: space-around;

      max-width: 1300px;
      margin: 0 auto;
      padding: 0 20px;

      .selected {
        a {
          color: #ff204b;
        }
        // border-bottom: 3px solid #ff204b;
      }
      a {
        color: #000;
        font-size: 17px;
        &:hover {
          color: #ff204b;
        }
      }

      div {
        width: 138px;
        height: 60px;
        line-height: 60px;
        font-weight: bold;
        text-align: center;
        cursor: pointer;
      }
    }
  }
}
</style>
