<template>
    <div class="order-detail">
        <div class="title"><span>주문상세조회</span></div>

        <span class="info-title">주문정보</span>
        <table class="info-box">
            <tr>
                <td>주문번호</td>
                <td>{{detailData.orderNum}}</td>
            </tr>
            <tr>
                <td>주문일자</td>
                <td>{{detailData.orderTime}}</td>
            </tr>
            <tr>
                <td>주문자</td>
                <td>{{detailData.orderName}}</td>
            </tr>
            <tr>
                <td>결제금액</td>
                <td>{{detailData.discountPrice | makeComma}} 원</td>
            </tr>
            <tr>
                <td>적립예정포인트</td>
                <td>0 원</td>
            </tr>
        </table>

        <span class="order-title">주문상품</span>
        <table class="order-list">
            <thead>
            <tr class="order-list-title">
                <td colspan="4">일반 배송</td>
            </tr>
            </thead>
            <tbody>
            <template v-for="product in detailData.product">
            <tr class="order-list-brand" :key="product">
                <td colspan="2">{{product.brand}}</td>
                <td>주문금액</td>
                <td>진행사항</td>
            </tr>

            <tr class="order-list-product" v-for="option in product.option" :key="option">
                <td>
                    <img :src="option.image" alt="">
                </td>
                <td>
                    <div>{{option.name}}</div>
                    <div>{{option.productColor}} / {{option.prodcutSize}} (일반배송)</div>
                </td>
                <td>
                    <span>{{option.totalPrice | makeComma}} 원</span>
                </td>
                <td>
                    <span>결재완료</span>
                </td>
            </tr>
            </template>
            </tbody>
        </table>

        <span class="buy-title">결재정보</span>
        <div class="buy-box">
            <div class="buy-info-box">
                <div>
                    <span>결재수단</span>
                    <span>신용카드</span>
                </div>
                <div>
                    <span>총 상품금액</span>
                    <span>{{detailData.discountPrice | makeComma}} 원</span>
                </div>
                <div>
                    <span>쿠폰 할인 금액</span>
                    <span>0 원</span>
                </div>
                <div>
                    <span>총 사용 포인트</span>
                    <span>0 원</span>
                </div>
                <div>
                    <span>배송비</span>
                    <span>0 원</span>
                </div>
            </div>
            <div class="buy-result-box">
                <span>총 주문 금액</span>
                <span>{{detailData.discountPrice | makeComma}} 원</span>
            </div>
        </div>

        <span class="info-title">배송지 정보</span>
        <table class="info-box">
            <tr>
                <td>수령인</td>
                <td>장성준</td>
            </tr>
            <tr>
                <td>휴대폰</td>
                <td>01012341234</td>
            </tr>
            <tr>
                <td>우편번호</td>
                <td>12345</td>
            </tr>
            <tr>
                <td>주소</td>
                <td>서울시 강남구 테헤란로</td>
            </tr>
            <tr>
                <td>나머지 주소</td>
                <td>브랜디 4층</td>
            </tr>
            <tr>
                <td>배송 요청사항</td>
                <td>일반배송: 문 앞에 놓아주세요.</td>
            </tr>
        </table>

        <button class="order-confirm-btn">주문/배송조회로 이동</button>
    </div>
</template>

<script>
import API from '@/service/util/service-api'
import SERVER from '@/config.js'

export default {
  data () {
    return {
      detailData: {}
    }
  },
  mounted () {
    // this.detailData = mockup.data
    // this.sizeData = mockup.sizeData
    // mockup.options
    API.methods
      .get(`${SERVER.IP}/mypage/order/1`)
      .then((res) => {
        // console.log(res.data.result)
        this.detailData = res.data.result.data
      })
      .catch(() => {
        // console.log(error)
        this.$router.push('/main')
        alert('존재하지 않는 서비스 상품입니다.')
      })
  }
}
</script>

<style lang="scss" scoped>
.order-detail{
    display: flex;
    justify-content: center;
    flex-direction: column;
    padding: 0 30px;
    color: black;

    .title {
        font-size: 30px;
        font-weight: 500;
        text-align: center;
        margin: 50px auto;
    }

    .info-title {
        display: inline-block;
        font-size: 25px;
        font-weight: 300;
        margin-bottom: 15px;
    }
    .info-box {
        width: 100%;
        border-top: solid 1px black;
        border-bottom: solid 1px black;
        margin-bottom: 70px;
        font-size: 17px;

        tr {
            td {
                padding: 15px 0;
                border-bottom: solid 1px rgb(228, 228, 228);
            }
            td:first-child {
                width: 20%;
                padding-left: 15px;
                font-weight: 600;
            }
            td:last-child {
                width: 80%;
                font-weight: 400;
            }
        }
        tr:last-child>td {
            border: 0;
        }
    }

    .order-title{
        display: inline-block;
        font-size: 25px;
        font-weight: 300;
        margin-bottom: 15px;
    }
    .order-list {
        width: 100%;
        border-top: solid 1px black;
        border-bottom: solid 1px black;
        text-align: center;
        margin-bottom: 70px;

        thead tr {
            border-bottom: solid 1px rgb(228, 228, 228);
        }
        // tr:last-child {
        //     border: 0;
        // }

        .order-list-title>td {
            font-size: 20px;
            font-weight: 600;
            padding: 20px 0;
            text-align: left;
        }
        .order-list-brand {
            font-size: 15px;

            td {
                padding: 20px 0;
            }
            td:first-child {
                font-size: 18px;
                font-weight: 600;
                text-align: left;
            }
        }
        .order-list-product {
            padding: 15px 0;

            td {
                padding: 15px 15px 15px 0;
            }
            td:nth-child(1) {
                width: 80px;
                height: 80px;
                overflow: hidden;

                img {
                width: 80px;
                height: auto;
                }
            }
            td:nth-child(2) {
                width: 60%;
                text-align: left;

                div:first-child {
                    font-size: 17px;
                }
                div:last-child {
                    color: rgb(135, 135, 135);
                }
            }
            td:nth-child(3) {
                font-size: 20px;
                font-weight: 600;
            }
            td:nth-child(4) {
                font-size: 20px;
                font-weight: 600;
            }
        }
    }

    .buy-title {
        display: inline-block;
        font-size: 25px;
        font-weight: 300;
        margin-bottom: 15px;
    }
    .buy-box {
        width: 100%;
        border-top: solid 1px black;
        border-bottom: solid 1px black;
        margin-bottom: 70px;
        font-size: 17px;

        .buy-info-box {
            border-bottom: solid 1px rgb(228, 228, 228);
            padding: 10px 0;
            div {
                display: flex;
                justify-content: space-between;
                padding: 10px 0;
                font-size: 15px;

                span:first-child {
                    padding-left: 20px;
                }
                span:last-child {
                    padding-right: 20px;
                }
            }
        }
        .buy-result-box {
            display: flex;
            justify-content: space-between;
            padding: 30px 20px;
            font-size: 25px;
            font-weight: 600;
            color: red;

            span:first-child {
                color: black;
            }
        }
    }

    .order-confirm-btn {
        background-color: black;
        color: white;
        width: 230px;
        padding: 10px 0;
        font-size: 17px;
        font-weight: 400;
        border: 0;
        border-radius: 5px;
        margin: 0 auto;
        margin-bottom: 70px;
    }
}
</style>
