<template>
  <div>
    <div class="pointContainer">
      <div class="pointTitle">point</div>
      <div class="currentPoint">
        <div>보유</div>
        <div class="point">{{ point }} Won</div>
      </div>
      <div class="pointRegist">
        <div>등록</div>
        <div class="registDetail">포인트코드 등록은 앱에서만 가능합니다.</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      point: 0
    }
  }
}
</script>

<style lang="scss" scoped>
.pointContainer {
  width: 1260px;

  .pointTitle {
    font-size: 26px;
    padding-bottom: 10px;
    border-bottom: 1px solid black;
  }

  .currentPoint {
    font-weight: bold;
    display: flex;
    padding: 20px;
    border-bottom: 1px solid lightgray;

    .point {
      margin-left: 140px;
      color: red;
    }
  }

  .pointRegist {
    display: flex;
    padding: 20px;
    border-bottom: 1.5px solid black;
    font-weight: bold;

    .registDetail {
      font-weight: normal;
      margin-left: 140px;
    }
  }
}
</style>
