<template>
  <div class="qna-register">
    <table>
      <tr>
        <td>질문유형</td>
        <td>
          <DropDown :items="deliveryMock" v-model="deliveryType"></DropDown>
        </td>
      </tr>
      <tr>
        <td>내용</td>
        <td>
          <textarea rows="5" cols="3" v-model="contents" placeholder="내용을 입력해주세요." nonesizing/>
        </td>
      </tr>
      <tr>
        <td>공개여부</td>
        <td><CheckBox v-model="isPrivate"></CheckBox>비공개</td>
      </tr>
    </table>
    <div>
      <button class="cancle">취소하기</button>
      <button class="ok" @click="sendData">등록하기</button>
    </div>
  </div>
</template>

<script>
import CheckBox from '@/service/Components/CheckBox'
import DropDown from '@/service/Components/DropDown'
// eslint-disable-next-line no-unused-vars
import SERVER from '@/config'
// eslint-disable-next-line no-unused-vars
import API from '@/service/util/service-api'

export default {
  data () {
    return {
      deliveryType: '',
      contents: '',
      // 삭제하기 이거!!
      isPrivate: false,
      deliveryMock: [{
        label: '집 앞에 놓고 가주세요.',
        key: '11'
      },
      {
        label: '등등등..',
        key: '12'
      }
      ]
    }
  },
  components: { CheckBox, DropDown },
  methods: {
    sendData () {
      API.methods
        .post(`${SERVER.IP}/products/question`, {
          question_type_id: this.deliveryType,
          contents: this.contents,
          is_private: this.isPrivate,
          product_id: this.$route.params.id
        })
        .then((res) => {
          console.log(res)
        })
        .catch(() => {
          // console.log(error)
          this.$router.push('/main')
          alert('존재하지 않는 서비스 상품입니다.')
        })
    }
  }
}
</script>

<style lang="scss" scoped>
.qna-register {
  display: flex;
  flex-wrap: wrap;
  background-color: #f7f7f7;
  border-top: solid #222222 1px;
  padding: 0 20px;
  margin-bottom: 40px;
  font-size: 18px;
  width: 100%;
  text-align: left;

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
