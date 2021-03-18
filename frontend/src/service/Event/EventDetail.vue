<template>
  <div>
    <section class="main">
      <main class="article">
        <img src="/images/erdetail.jpeg">
        <div class="productBox">
          <ProductBox :product="product" v-for="product in productList" :key="product"></ProductBox>
        </div>
      </main>
    </section>
  </div>
</template>

<script>
import { ClientId, SERVER_IP } from '@/config.js'
import axios from 'axios'
import ProductBox from '@/service/Components/ProductBox'
// import Footer from '@/service/Components/Footer'
import { mapMutations } from 'vuex'
import mockup from '@/Data/ProductList.json'

const serviceStore = 'serviceStore'

export default {
  components: {
    // Footer
    ProductBox
  },
  data () {
    return {
      productList: mockup.data,
      // 구글 로그인 하기
      params: {
        client_id: ClientId
      },
      renderParams: {
        width: 250,
        height: 50,
        longtitle: true
      }
    }
  },
  methods: {
    ...mapMutations(serviceStore, ['getStorageToken']),

    onSuccess (googleUser) {
      localStorage.setItem('user_id', googleUser.tt.Ad)
      localStorage.setItem('user_email', googleUser.tt.bu)

      // axios 사용함에 있어 body에 빈 객체를 넣어야 post에서 headers의 정보를 보내기가 가능하다.
      const data = {}
      const headers = {
        headers: { Authorization: googleUser.wc.id_token }
      }
      axios
        .post(`${SERVER_IP}/user/google-signin`, data, headers)
        .then((res) => {
          if (res.data.access_token) {
            localStorage.setItem('access_token', res.data.access_token)
            this.getStorageToken()
            this.$router.push('/main')
          } else {
            alert('로그인 정보가 맞지 않습니다. 다시 시도해주세요.')
          }
        })
    },
    linkToSignUp () {
      if (this.getToken) {
        localStorage.removeItem('user_id')
        localStorage.removeItem('access_token')
        localStorage.removeItem('user_email')
        this.getStorageToken()
        this.$route.path !== '/main' && this.$router.push('/main')
      } else {
        this.$route.path !== '/signup' && this.$router.push('/signup')
      }
    },
    linkToEventDetail () {
      this.$router.push('/event/100')
    }
  }
}
</script>

<style lang="scss" scoped>
.main {
  .article {
    width: 1240px;
    margin: 50px auto 50px auto;
    // display: flex;
    // flex-direction: column;
    // align-items: center;
    text-align: center;
    > img {
      width: 100%;
    }
  }
}
</style>
