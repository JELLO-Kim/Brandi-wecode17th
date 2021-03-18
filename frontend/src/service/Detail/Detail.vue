<template>
  <main>
    <article class="ProductInfo">
      <agile v-if="detailData.image_list[1]" class="agile" :dots="false">
        <div class="imgContainer">
          <img alt="product  image" :src="detailData.image_list[0]" />
        </div>
        <div v-if="detailData.image_list[1]" class="imgContainer">
          <img alt="product  image" :src="detailData.image_list[1]" />
        </div>
        <div v-if="detailData.image_list[2]" class="imgContainer">
          <img alt="product  image" :src="detailData.image_list[2]" />
        </div>
        <div v-if="detailData.image_list[3]" class="imgContainer">
          <img alt="product  image" :src="detailData.image_list[3]" />
        </div>
        <div v-if="detailData.image_list[4]" class="imgContainer">
          <img alt="product  image" :src="detailData.image_list[4]" />
        </div>
        <div class="prevBtn" slot="prevButton" />
        <div class="nextBtn" slot="nextButton" />
      </agile>
      <div v-else class="imgContainer">
        <img alt="product  image" :src="detailData.image_list[0]" />
      </div>
      <div class="detailInfoContainer">
        <p class="title">{{ detailData.name }}</p>
        <div class="priceContainer">
          <span v-if="detailData.discount_rate" class="percent"
            >{{ detailData.discount_rate }}%</span
          >
          <span class="price">
            {{ parseInt(detailData.sales_price).toLocaleString() + "원" }}
          </span>
          <span v-if="detailData.discount_rate !== 0" class="cost">{{
            Math.floor(detailData.original_price).toLocaleString(5) + "원"
          }}</span>
        </div>
        <hr />
        <div v-on:click="onColorClick" class="option">
          <div>{{ colorToggleData }}</div>
          <div class="imgContainer">
            <img
              src="https://www.brandi.co.kr/static/3.49.1/images/ic-arrow-bl-down@3x.png"
            />
          </div>
          <div
            v-bind:class="{
              toggleOn: isColorToggle,
              toggleOff: !isColorToggle,
            }"
          >
            <div class="defaultToggle">[색상]을 선택하세요.</div>
            <div
              v-for="(item, index) in detailData.colors"
              class="colorToggle"
              v-bind:key="index"
              @click="colorClickHandler(item, index)"
            >
              {{ item.color_name }}
            </div>
          </div>
        </div>
        <!-- 사이즈 옵션 -->
        <div v-on:click="onSizeClick" class="option">
          <div
            v-bind:class="{
              optionTitle: disabledSizeToggle,
              none: !disabledSizeToggle,
            }"
          >
            {{ sizeToggleData }}
          </div>
          <div class="imgContainer">
            <img
              src="https://www.brandi.co.kr/static/3.49.1/images/ic-arrow-bl-down@3x.png"
            />
          </div>
          <div
            v-bind:class="{
              toggleOn: isSizeToggle,
              toggleOff: !isSizeToggle,
            }"
          >
            <div class="defaultToggle">[사이즈]를 선택하세요.</div>
            <div
              v-for="(item, index) in sizeData"
              class="colorToggle"
              v-bind:key="index"
              @click="optionSizeHandler(sizeData, index)"
            >
              {{ item.size }}
            </div>
          </div>
        </div>
        <div
          v-bind:class="{
            selectedOptions: isPurchaseBox,
            noneOptions: !isPurchaseBox,
          }"
        >
          <div class="selectTitle">
            <p>{{ purchaseColor }} / {{ purchaseSize }}</p>
            <div @click="removeSelectHandler()" class="imgContainer">
              <img
                src="https://www.brandi.co.kr/static/3.49.1/images/img_icon_x.png"
              />
            </div>
          </div>
          <div class="selectPrice">
            <div class="selectQuantity">
              <button
                class="quantityControlBtn"
                name="minus"
                @click="selectQuantityHandler"
              >
                -
              </button>
              <input class="productQuantity" :value="input" readonly />
              <button
                class="quantityControlBtn"
                name="plus"
                @click="selectQuantityHandler"
              >
                +
              </button>
            </div>
            <p>
              {{
                (parseInt(detailData.sales_price) * input).toLocaleString() +
                  "원"
              }}
            </p>
          </div>
        </div>
        <div class="detailpriceContainer">
          <p>총 {{ input }}개의 상품</p>
          <p class="totalPrice">
            총 금액
            <strong v-if="detailData">
              {{
                (parseInt(detailData.sales_price) * input).toLocaleString() +
                  "원"
              }}
            </strong>
          </p>
        </div>
        <button @click="buyNowHandler" class="purchaseBtn">
          바로 구매하기
        </button>
        <button type="button" class="cartBtn">장바구니 담기</button>
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
        <div>
          <div class="detailHtml" v-html="detailData.html" />
        </div>
        <div>
          <QnA></QnA>
        </div>
      </div>
    </article>
  </main>
</template>

<script>
// import { SERVER_IP } from '@/config.js'
// import axios from 'axios'
import { VueAgile } from 'vue-agile'
import QnA from './QnA'
import mockup from '@/Data/DetailOption.json'

export default {
  components: {
    // 이미지 Caroucel
    agile: VueAgile,
    QnA
  },
  created () {
    this.detailData = mockup.data
    // this.sizeData = mockup.sizeData
    // mockup.options
    // axios
    //   .get(`${SERVER_IP}/product/${this.$route.params.id}`)
    //   .then((res) => {
    //     this.detailData = res.data.data
    //     this.purchaseId = this.detailData.product_id
    //   })
    // .catch((error) => {
    //   this.$router.push('/main')
    //   alert('존재하지 않는 서비스 상품입니다.')
    // })
  },

  data () {
    return {
      detailData: {
        colors: [],
        discount_rate: 0,
        html: '',
        image_list: [],
        max_sales_quantity: 20,
        min_sales_quantity: 1,
        name: '',
        original_price: 0,
        product_id: 0,
        sales_price: 0
      },
      colorToggleData: '[색상]을 선택하세요.',
      isColorToggle: false,
      sizeToggleData: '[사이즈]를 선택하세요.',
      isSizeToggle: false,
      disabledSizeToggle: false,
      input: 0,
      isPurchaseBox: false,
      purchaseColor: '',
      purchaseColorId: '',
      purchaseSize: '',
      purchaseSizeId: '',
      purchaseId: '',
      colorData: [],
      sizeData: [],
      productQuantity: 0,
      noneDisplay: false
    }
  },
  methods: {
    colorClickHandler (item, index) {
      // 중복된 통신은 한번만 처리하도록 함
      if (this.colorToggleData === item.color_name) {
        return
      }

      this.colorToggleData = item.color_name
      this.purchaseColorId = item.color_id
      this.sizeData = item.sizes

      // axios
      //   .get(
      //     `${SERVER_IP}/product/${this.$route.params.id}?color_id=${item.color_id}`
      //   )
      //   .then((res) => {
      //     this.sizeData = res.data.data
      //   })
    },

    // 컬러 인풋 클릭시 토글 박스 열리게하기
    onColorClick () {
      this.isColorToggle = !this.isColorToggle

      if (this.colorToggleData !== '[색상]을 선택하세요.') {
        this.disabledSizeToggle = !this.disabledSizeToggle
      }

      this.isSizeToggle = false
    },

    // 사이즈 인풋클릭시 토글 박스 열리게하기
    onSizeClick () {
      if (this.colorToggleData !== '[색상]을 선택하세요.') {
        this.isSizeToggle = !this.isSizeToggle
      }
    },

    // 옵션 사이즈 토글에서 원하는 사이즈 선택시 적용
    optionSizeHandler (colorData, index) {
      this.productQuantity = colorData[index].quantity
      this.sizeToggleData = colorData[index].size
      this.purchaseInputNumber = this.input
      this.input = 1
      this.purchaseColor = this.colorToggleData
      this.purchaseSize = this.sizeToggleData
      this.purchaseSizeId = colorData[index].size_id
      this.colorToggleData = '[색상]을 선택하세요.'
      this.sizeToggleData = '[사이즈]를 선택하세요.'
      this.isSizeToggle = false
      this.isPurchaseBox = true
    },

    // 상품 수량 조절하여 갯수 띄워주기
    // +와 - 버튼을 클릭하여 조절한다.
    // 최소,최대값 안의 input 값이라면 +, - 동작
    selectQuantityHandler (e) {
      const { name } = e.target
      const isPlus = name === 'plus'

      if (!isPlus && this.input <= 1) return
      if (isPlus && this.input >= 20) { return alert('최대 구매 수량은 20개 입니다.') }
      if (isPlus && this.input >= this.productQuantity) { return alert(`상품의 재고 수량은 ${this.productQuantity}개 입니다.`) }

      isPlus ? (this.input += 1) : (this.input -= 1)
    },

    // 삭제하기 버튼 클릭시 상품 구매 박스를 안보이게 적용
    removeSelectHandler () {
      if (confirm('정말 삭제하시겠습니까?')) {
        this.isPurchaseBox = false
        this.input = 0
      } else {

      }
    },

    // 상품구매하기 버튼을 클릭하여 로컬스토리지 저장후 구매하기 페이지로 이동
    // 상품의 갯수가 0이라면 return
    buyNowHandler () {
      if (this.input === 0) {
        alert('상품을 선택해주세요.')
        return
      }

      localStorage.setItem('purchaseColor', this.purchaseColorId)
      localStorage.setItem('purchaseSize', this.purchaseSizeId)
      localStorage.setItem('purchaseProductNumber', this.input)
      localStorage.setItem('purchaseId', this.purchaseId)

      this.$router.push('/order')
    }
  }
}
</script>

<style lang="scss">
/* .noneDisplay {
  width: 100%;
  height: 100%;
  background-color: black;
} */

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
    width: 100%;
    /* height: 100%; */
    // border-bottom: 2px solid #dbdbdb;

    .tabs {
      position: sticky;
      top: 0;
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
