<template>
  <div class="qna-register">
    <table>
      <tr>
        <td>질문유형</td>
        <td>
          <select>
            <option>질문유형을 선택하세요</option>
            <option>상품 문의</option>
          </select>
        </td>
      </tr>
      <tr>
        <td>내용</td>
        <td>
          <textarea rows="5" cols="3" placeholder="내용을 입력해주세요." nonesizing/>
        </td>
      </tr>
      <tr>
        <td>공개여부</td>
        <td><label><input type="checkbox">비공개</label></td>
      </tr>
    </table>
    <div>
      <button class="cancle">취소하기</button>
      <button class="ok">등록하기</button>
    </div>
  </div>
</template>

<script>
export default {

}
</script>

<style lang="scss" scoped>
.qna-register {
  display: block;
  background-color: #f7f7f7;
  border-top: solid #222222 1px;
  padding: 0 20px;
  margin-bottom: 40px;
  font-size: 18px;

  table {
    color: black;
    width: 100%;
    // border-collapse: separate;
    // border-spacing: 0 30px;

    tr {
      width: 100%;
      border-bottom: solid 1px rgb(228, 228, 228);
    }

    td {
      padding: 20px;
      display: inline-block;
    }
    tr>td:first-child {
      font-weight: 400;
      width: 10%;
    }
    tr>td:last-child {
      width: 90%;

      textarea, select, option {
        width: 100%;
        border: solid 1px rgb(228, 228, 228);
        border-radius: 5px;
        padding: 15px;
      }

      input {
        margin-right: 10px;
      }
    }
  }

  div:last-child {
    text-align: center;

    button {
      font-weight: 600;
      border-radius: 10px;
      border: solid 1px #1f1f1f;
      padding: 15px 45px;
      margin: 30px 5px;
    }
    button:first-child {
      background-color: white;
      color: #1f1f1f;
    }
    button:last-child {
      background-color: #1f1f1f;
      color: white;
    }
  }
}

</style>
