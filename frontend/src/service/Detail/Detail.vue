<template>
  <main>
    <article class="ProductInfo">
      <agile v-if="detailData.imageList[0]" class="agile" :dots="false">
        <div class="imgContainer">
          <img alt="product  image" :src="detailData.imageList[0]" />
        </div>

        <div v-for="image in detailData.imageList" class="imgContainer" :key="image">
          <img alt="product image" :src="image" />
        </div>

        <div class="prevBtn" slot="prevButton" />
        <div class="nextBtn" slot="nextButton" />
        <!-- 이거 작은 이미지 리스트 한번 봐야함! -->
        <!-- <div class="smallImage"></div> -->
      </agile>

      <div class="detailInfoContainer">
        <p class="title">{{ detailData.name }}</p>
        <div class="priceContainer">
          <span v-if="detailData.discountRate" class="percent">
            {{ detailData.discountRate }}%
          </span>
          <span class="price">
            {{ detailData.price | makeComma }}원
          </span>
          <span v-if="detailData.discountRate !== 0" class="cost">
            {{ detailData.discountPrice | makeComma }}원
          </span>
        </div>
        <hr />

        <DropDown :items="detailData.colors" v-model="color" @change="selectOption" placeholder="[색상]을 선택하세요." class="option-box"></DropDown>
        <DropDown :items="detailData.sizes" v-model="size" @change="selectOption" placeholder="[사이즈]를 선택하세요." class="option-box"></DropDown>

        <div class="option-quantity">
          <OptionQuantity v-for="item in optionQuantity" :item="item" :key="item" @remove="removeOption"></OptionQuantity>
        </div>

        <div class="detailpriceContainer">
          <p>총 {{ totalCount }}개의 상품</p>
          <p class="totalPrice">
            총 금액
            <strong v-if="detailData">
              {{
                totalPrice | makeComma
              }}원
            </strong>
          </p>
        </div>
        <button @click="buyNowHandler" class="purchaseBtn">
          바로 구매하기
        </button>
        <button type="button" class="cartBtn" @click="addCart">장바구니 담기</button>
      </div>
    </article>
    <article class="detailProduct">
      <div class="categoryContainer">
        <div class="tabs">
          <div class="tab productDetail selected"><a href="#">상품정보</a></div>
          <div class="tab review"><a href="#">리뷰</a></div>
          <div class="tab qna"><a href="#">Q&A</a></div>
          <div class="tab orderDetail"><a href="#">주문정보</a></div>
        </div>
        <div class="detail-body">
          <div class="detailHtml" v-html="detailData.productContentImage" />
        </div>
        <div>
          <QnA v-bind:isMypage="isMypage" v-bind:title="title"></QnA>
        </div>
      </div>
    </article>
    <!-- <Toast :message="errorMessage" v-on:remove-message="removeMessage"/> -->
  </main>
</template>

<script>
import SERVER from '@/config.js'
import API from '@/service/util/service-api'
import { VueAgile } from 'vue-agile'
import QnA from './QnA'
import DropDown from '@/service/Components/DropDown'
import OptionQuantity from './OptionQuantity'
// import mockup from '@/Data/Detail.json'
import { mapMutations, mapGetters } from 'vuex'
// import Toast from '@/service/Components/Toast'

const serviceStore = 'serviceStore'

export default {
  components: {
    // 이미지 Caroucel
    agile: VueAgile,
    QnA,
    DropDown,
    OptionQuantity
    // Toast
  },
  mounted () {
    // this.detailData = mockup.data
    // this.sizeData = mockup.sizeData
    // mockup.options
    API.methods
      .get(`${SERVER.IP}/products/${this.$route.params.id}`)
      .then((res) => {
        // console.log(res.data.result)
        this.detailData = res.data.result.product
      })
      .catch(() => {
        // console.log(error)
        this.$router.push('/main')
        alert('존재하지 않는 서비스 상품입니다.')
      })
  },
  props: {
    id: String
  },
  data () {
    return {
      color: null,
      size: null,
      optionQuantity: [],
      sellerProducts: [],
      qnaList: [],
      detailData: {
        id: 0,
        colors: [],
        sizes: [],
        name: '',
        productContentImage: '',
        imageList: [],
        maximum: 0,
        minimum: 0,
        price: 0,
        discountPrice: 0,
        discountRate: 0
      },
      isMypage: false,
      title: 'Q&A',
      errorMessage: ''
    }
  },
  computed: {
    ...mapGetters(serviceStore, ['getToken']),
    // 이건 한번 봐야함!!
    colorList () {
      const res = []
      for (const key in this.detailData.colors) {
        res.push({ key: this.detailData.colors[key].color_name, label: this.detailData.colors[key].color_name })
      }
      return res
    },
    totalPrice () {
      let total = 0
      this.optionQuantity.forEach(d => {
        total += d.quantity * d.price
      })
      return total
    },
    totalCount () {
      let total = 0
      this.optionQuantity.forEach(d => {
        total += d.quantity
      })
      return total
    }
  },
  methods: {
    ...mapMutations(serviceStore, ['getStorageToken']),

    selectOption () {
      if (this.color && this.size) {
        const colorItem = this.detailData.colors.find(d => d.key === this.color)
        const sizeItem = this.detailData.sizes.find(d => d.key === this.size)

        const item = this.optionQuantity.find(d => this.size === d.size && this.color === d.color)
        // 동일 옵션이 있다면
        if (item) {
          item.quantity += 1
        } else {
          this.optionQuantity.push({
            size: this.size,
            color: this.color,
            sizeName: sizeItem.label,
            colorName: colorItem.label,
            price: this.detailData.discountPrice,
            quantity: 1
          })
        }
        this.color = null
        this.size = null
      }
    },
    removeOption (item) {
      const pos = this.optionQuantity.indexOf(item)
      if (pos >= 0) {
        this.optionQuantity.splice(pos, 1)
      }
    },
    // 상품구매하기 버튼을 클릭하여 로컬스토리지 저장후 구매하기 페이지로 이동
    // 상품의 갯수가 0이라면 return
    buyNowHandler () {
      if (this.optionQuantity.length > 0) {
        if (this.getToken) {
          const orderData = {
            productId: this.id,
            products: this.optionQuantity
          }

          localStorage.setItem('items', orderData)
          this.$router.push('/order')
        } else {
          alert('로그인이 필요한 서비스입니다.')
          this.$router.push('/login')
        }
      } else {
        this.$toast.open({
          message: '옵션을 한개 이상 선택해주세요.',
          position: 'bottom',
          duration: 3000,
          type: 'default'
        })
      }
    },

    // 내가 짠 코드!
    addCart () {
      console.log('이거 눌림???')
      if (this.optionQuantity.length > 0) {
        if (this.getToken) {
          API.methods.post(`${SERVER.IP}/cart`, this.optionQuantity)
            .then((res) => {
              if (res.message === 'SUCCESS') this.errorMessage = '선택한 상품이 장바구니에 담겼습니다.'
            })
            .catch((error) => {
              alert(error.message)
            })
        } else {
          alert('로그인이 필요한 서비스입니다.')
          this.$router.push('/login')
        }
      } else {
        this.errorMessage = '옵션을 한개 이상 선택해주세요.'
      }
    },

    removeMessage () {
      this.errorMessage = ''
    }
  }
}
</script>

<style lang="scss" scoped>

.option-box {
  margin: 5px 0;
}
.option-quantity {
  margin: 20px 0;
}

.ProductInfo {
  width: 1235px;
  margin: 80px auto 80px;
  display: flex;

  .agile {
    width: 546px;
    height: 546px;
    position: relative;

    .prevBtn {
      width: 32px;
      height: 32px;
      background-position: 0 0;
      left: 10px;
      top: 240px;
      position: absolute;
      background-image: url(https://www.brandi.co.kr/static/3.49.1/images/controls.png);
    }

    .nextBtn {
      width: 32px;
      height: 32px;
      background-position: -32px 0;
      right: 10px;
      top: 240px;
      position: absolute;
      background-image: url(https://www.brandi.co.kr/static/3.49.1/images/controls.png);
    }
  }

  .imgContainer {
    width: 546px;
    height: 546px;

    img {
      width: 100%;
      height: 100%;
    }
  }

  .detailInfoContainer {
    width: 53%;
    font-family: "Spoqa Han Sans", Sans-serif;
    margin-left: 50px;

    .title {
      font-size: 24px;
      line-height: 150%;
    }

    .priceContainer {
      margin: 16px 0 30px;

      .percent {
        font-size: 26px;
        font-weight: bold;
        color: #ff204b;
      }

      .price {
        font-size: 26px;
        font-weight: bold;
      }

      .cost {
        font-size: 20px;
        font-weight: 500;
        text-decoration: line-through;
        color: #929292;
      }
    }

    #none {
      cursor: default;
    }

    .option {
      height: 48px;
      border: 1px solid #e1e1e1;
      font-size: 13px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 10px;
      padding: 0 10px;
      position: relative;
      cursor: pointer;

      .none {
        color: #929292;
        font-size: 13px;
        cursor: default;
      }

      .optionTitle {
        color: black;
        font-size: 13px;
      }

      .toggleOff {
        display: none;
      }

      .toggleOn {
        width: 639px;
        top: 46.5px;
        left: -1px;
        position: absolute;
        z-index: 99;
        font-size: 13px;
        background-color: white;
        border: 1px solid #e1e1e1;

        .defaultToggle {
          height: 42px;
          opacity: 0.35;
          padding: 13px 10px 0;
        }

        .colorToggle {
          height: 42px;
          padding: 13px 10px 0;

          &:hover {
            background-color: #f8f8f8;
          }
        }
      }

      .imgContainer {
        width: 18px;
        height: 10px;

        img {
          width: 100%;
          height: 100%;
        }
      }
    }

    .detailpriceContainer {
      display: flex;
      justify-content: space-between;
      margin-top: 30px;
      font-weight: bold;
      font-size: 16px;

      .totalPrice {
        font-size: 20px;

        strong {
          color: #ff204b;
        }
      }
    }

    .noneOptions {
      display: none;
    }

    .selectedOptions,
    .noneOptions {
      height: 120px;
      border: 1px solid #f1f1f1;
      background-color: #fafafa;
      padding: 25px 20px 0;
      margin-top: 20px;

      .selectTitle {
        display: flex;
        justify-content: space-between;
        margin-bottom: 20px;

        .imgContainer {
          width: 16px;
          height: 16px;
          cursor: pointer;

          img {
            width: 100%;
            height: 100%;
          }
        }
      }

      .selectPrice {
        display: flex;
        justify-content: space-between;

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

    .purchaseBtn, .cartBtn {
      width: 180px;
      height: 50px;
      background: black;
      color: white;
      border-radius: 5px;
      margin-top: 30px;
      outline: none;
      border: none;
      cursor: pointer;
    }
    .cartBtn {
      width: 60px;
      // font-size: 0;
      text-indent: -1000em;
      background: #FFF url(/images/btn-cart.svg) 50% 50% no-repeat;
      border: 1px solid #CCC;
    }
  }
}

.detailProduct {
  width: 1235px;
  margin: 0px auto 100px;
  display: flex;

  .categoryContainer {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    width: 100%;
    /* height: 100%; */
    // border-bottom: 2px solid #dbdbdb;
    .detail-body {
      text-align: center;
    }

    .tabs {
      position: sticky;
      top: 0;
      width: 100%;
      height: 50px;
      background: #FFF;
      display: flex;
      .tab {
        width: 25%;
        // width: 250px;
        height: 50px;
        line-height: 50px;
        text-align: center;
        border-bottom: 1px solid #ccc;
        a {
          color: #000;
          font-size: 16px;
          display: inline-block;
          width: 100%;
          height: 100%;
          &:hover {
            color: #ff204b;
          }
        }
        &.selected {
          a {
            color: #ff204b;
          }
          // margin-left: 30px;
          // padding-top: 15px;
          border-bottom: 2px solid #ff204b;
          // text-align: center;
        }
      }

    }

    .detailContents {
      margin-top: 40px;
      font-size: 14px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      text-align: center;
    }
  }
}
</style>
