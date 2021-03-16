<template>
  <div>
    <div class="couponContainer">
      <div class="couponTop">
        <div class="title">
          <div>발급받은 쿠폰</div>
          <div class="number">{{ coupon }}</div>
        </div>
        <span>* 유효기간이 30일 지난 쿠폰은 목록에서 삭제됩니다</span>
      </div>
      <div class="couponList">
        발급받은 쿠폰이 존재하지 않습니다.
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      coupon: 0
    }
  }
}
</script>

<style lang="scss" scoped>
.couponContainer {
  width: 1260px;

  .couponTop {
    display: flex;
    align-items: baseline;
    border-bottom: 1px solid black;

    span {
      font-size: 14px;
    }
    .title {
      display: flex;
      margin-bottom: 10px;
      div {
        font-size: 25px;
      }
      .number {
        font-weight: bold;
        margin: 0 5px;
      }
    }
  }

  .couponList {
    text-align: center;
    font-size: 17px;
    padding: 10px 0;
    border-bottom: 1px solid lightgray;
  }
}
</style>
