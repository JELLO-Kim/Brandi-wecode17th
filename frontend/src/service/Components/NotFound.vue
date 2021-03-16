<template>
  <div>
    <div class="article">
      <div class="errorContainer">
        <img src="Images/warning.png" />
        <div class="warningTitle">찾을 수 없는 페이지 입니다.</div>
        <div class="warningBox">
          <div>
            <div>브랜디를 찾아주신 고객님. 이용에 불편을 드려 죄송합니다.</div>
            <div>입력하신 페이지의 주소가 잘못 입력되었거나, 변경 또는 삭제되어 요청하신 페이지를 찾을 수 없습니다.</div>
            <div>입력하신 주소가 정확한지 다시 한번 확인해주시기 바랍니다.</div>
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
      height: 200px;
      width: 650px;
      border: 1px solid lightgray;
      background-color: rgb(244, 244, 244);

      div {
        margin: 20px 0;
      }
    }
  }
}
</style>
