<template>
  <div>
    <section class="main">
      <main class="article">
        <h1 class="loginTitle">회원가입</h1>
        <h2 class="subLoginTitle">브랜디/하이버의 통합회원으로 가입됩니다.</h2>
        <div class="loginContainer">
          <h3>아이디 <span class="required">(필수)</span></h3>
          <input class="loginInput" placeholder="아이디 입력" />
          <h3>이메일 <span class="required">(필수)</span></h3>
          <input class="loginInput" placeholder="이메일 입력" />
          <h3>비밀번호 <span class="required">(필수)</span></h3>
          <input class="loginInput" placeholder="비밀번호 입력" type="password" />
          <input class="loginInput" placeholder="비밀번호 재입력" type="password" />
          <h3>휴대폰 번호 <span class="required">(필수)</span></h3>
          <div class="phonenumber">
            <input class="loginInput" placeholder="010" maxlength="3" />
            <input class="loginInput" placeholder="0000"  maxlength="4" />
            <input class="loginInput" placeholder="0000"  maxlength="4" />
            <button type="button">인증요청</button>
          </div>
          <h3>생년월일</h3>
          <div class="birthday">
            <input class="loginInput" placeholder="년도" maxlength="4" />
            <input class="loginInput" placeholder="월" maxlength="2" />
            <input class="loginInput" placeholder="일" maxlength="2" />
          </div>
          생년월일을 입력해주시면 회원가입 쿠폰이 지급됩니다.

          <h3>추천인 코드</h3>
          <input class="loginInput" placeholder="추천인코드 입력 (선택)" />
          추천인 코드를 입력하시면, 친구초대 포인트가 지급됩니다.

          <hr>

          <h3><label><input type="checkbox" v-model="allMark" /> 약관 모두 동의</label></h3>
          <div class="agreement">
            <div class="line">
              <label>
                <input type="checkbox" v-model="marks.mark1">
                만 14세 이상입니다 <span class="required">(필수)</span>
              </label>
            </div>
            <div class="line">
              <label>
                <input type="checkbox" v-model="marks.mark2">
                브랜디 약관 동의 <span class="required">(필수)</span>
              </label>
              <a class="more">내용보기</a>
            </div>
            <div class="line">
              <label>
                <input type="checkbox" v-model="marks.mark3">
                개인정보수집 및 이용에 대한 안내 <span class="required">(필수)</span>
              </label>
              <a class="more">내용보기</a>
            </div>
            <div class="line">
              <label>
                <input type="checkbox" v-model="marks.mark4">
                이벤트/마케팅 수신 동의 (선택)
              </label>
              <a class="more">내용보기</a>
            </div>
            <div class="line">
              <label>
                <input type="checkbox" v-model="marks.mark5">
                야간 혜택 알림 수신 동의 (선택)
              </label>
              <a class="more">내용보기</a>
            </div>
          </div>

          <button type="button" class="loginBtn" :disabled="!canRegister">가입하기</button>
        </div>
      </main>
    </section>
  </div>
</template>

<script>
import { ClientId, SERVER_IP } from '@/config.js'
// import { GoogleLogin } from 'vue-google-login'
import axios from 'axios'
// import Footer from '@/service/Components/Footer'
import { mapMutations } from 'vuex'

const serviceStore = 'serviceStore'

export default {
  components: {
    // GoogleLogin
    // Footer
  },
  data () {
    return {
      // 구글 로그인 하기
      params: {
        client_id: ClientId
      },
      renderParams: {
        width: 250,
        height: 50,
        longtitle: true
      },
      marks: {
        mark1: false,
        mark2: false,
        mark3: false,
        mark4: false,
        mark5: false
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
    }
  },
  mounted () {
    // console.log(this.$refs)
  },
  computed: {
    canRegister () {
      return this.marks.mark1 && this.marks.mark2 && this.marks.mark3
    },
    allMark: {
      get () {
        for (const key in this.marks) {
          if (!this.marks[key]) return false
        }
        return true
      },
      set (v) {
        for (const key in this.marks) {
          this.marks[key] = v
        }
      }
    }
  }
}
</script>

<style lang="scss" scoped>
span.required {
  color: red;
}
.main {
  .article {
    width: 1300px;
    margin: 50px auto 0;
    display: flex;
    flex-direction: column;
    align-items: center;

    h3 > label > input[type=checkbox]::after {
      top: -8px;
    }
    label {
      > input[type=checkbox] {
        width: 30px;
        &:checked::after {
          border-color: #000;
          color: #000;
        }
        &::after{
          top: -3px;
          position: relative;
          opacity: 1;
          display: inline-block;
          content: "V";
          color: #DDD;
          line-height: 22px;
          font-size: 10px;
          text-align: center;
          width: 22px;
          height: 22px;
          border: 2px solid #DDD;
          border-radius: 5px;
          background: #FFF;
        }
      }
    }

    .loginTitle {
      font-size: 34px;
      font-weight: bold;
      margin-bottom: 5px;
      color: #000;
      font-family: "Spoqa Han Sans", Sans-serif;
    }

    .subLoginTitle {
      margin-top: 5px;
      font-size: 18px;
      font-weight: 100;
      font-family: "Spoqa Han Sans", Sans-serif;
    }

    .loginContainer {
      width: 600px;
      margin-top: 20px;
      margin-bottom: 50px;
      display: flex;
      flex-direction: column;
      justify-content: center;

      ::placeholder {
        color: #CCC;
        font-size: 16px;
        // font-style: italic;
      }
      h3 {
        font-size: 18px;
        margin: 20px 0 5px 0;
      }
      .phonenumber {
        display: flex;
        flex-direction: row;
        .loginInput {
          width: 27%;
          margin: 0 5px;
          text-align: center;
          border-radius: 5px;
          &:first-child {
            margin-left: 0;
          }
        }
        button {
          width: 19%;
          border: 1px solid #000;
          border-radius: 5px;
          background: #FFF;
        }
      }
      .birthday {
        display: flex;
        flex-direction: row;
        .loginInput {
          width: 33%;
          margin: 0 5px;
          text-align: center;
          &:first-child {
            margin-left: 0;
          }
        }
      }

      .loginInput {
        height: 50px;
        border: 1px solid lightgray;
        border-radius: 3px;
        margin: 5px 0;
        padding: 10px;
        outline: none;
        font-size: 14px;
        font-weight: 500;
        color: #333333;
      }

      .loginBtn {
        height: 50px;
        border: none;
        line-height: 50px;
        margin-top: 14px;
        font-size: 13px;
        text-align: center;
        border-radius: 4px;
        background-color: black;
        color: white;
        cursor: pointer;
        &:disabled {
          background-color: #666;
        }
      }

      .joinBtn {
        height: 50px;
        line-height: 50px;
        margin-top: 4px;
        font-size: 13px;
        text-align: center;
        border: 1px solid black;
        border-radius: 4px;
        cursor: pointer;
      }

      .loginFind {
        text-align: right;
        padding: 17px 0;
        font-size: 13px;
        color: #666;
        border-bottom: 1px solid #ccc;

        .findId,
        .findPw {
          cursor: pointer;
        }

        .border {
          margin: 0 10px;
          border-right: 1px solid #ccc;
        }
      }

      .socialTitle {
        margin: 35px 0 15px;
        text-align: center;
        font-weight: bold;
        font-size: 16px;
      }

      .googleLogin {
        width: 278px;
        height: 50px;
        background-color: white;
        border: 1px solid #bdbdbd;
        border-radius: 5px;
        margin: 0 auto 50px;
        font-weight: 500;
        color: #666;
        display: flex;
        justify-content: center;
        align-items: center;
        cursor: pointer;

        &:hover {
          color: white;
          background-color: black;
        }

        .imgContainer {
          width: 28px;
          height: 28px;
          margin-right: 10px;

          img {
            width: 100%;
            height: 100%;
          }
        }
      }

      hr {
        width: 100%;
        margin: 30px 0;
        border: none;
        border-top: 2px solid #F1F1F1;
      }

      .agreement {
        border: 1px solid #CCC;
        border-radius: 20px;
        padding: 20px 30px;
        .line {
          margin: 10px 0;
          display: flex;
          justify-content: space-between;
          label {
            font-size: 16px;
          }
          .more {
            color: #666;
          }
        }
      }
    }
  }
}
</style>
