<template>
  <div>
    <div class="article">
      <div class="errorContainer">
        <img src="Images/warning.png" />
        <div class="warningTitle">네트워크에 문제가 발생하였습니다.</div>
        <div class="warningBox">
          <div>
            <div>브랜디를 찾아주신 고객님. 이용에 불편을 드려 죄송합니다.</div>
            <div>이용하시는 환경의 네트워크 문제가 발생하였습니다. 잠시 후 이용 바랍니다.</div>
            <div>감사합니다.</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {}
</script>

<style lang="scss" scoped>
.article {
  display: flex;
  justify-content: center;

  .errorContainer {
    margin: 70px 0;
    text-align: center;

    .warningTitle {
      font-size: 30px;
      margin: 30px 0;
    }

    .warningBox {
      padding: 0 20px;
      display: flex;
      align-items: center;
      text-align: left;
      height: 150px;
      width: 600px;
      border: 1px solid lightgray;
      background-color: rgb(244, 244, 244);

      div {
        margin: 20px 0;
      }
    }
  }
}
</style>
