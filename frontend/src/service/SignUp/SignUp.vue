<template>
  <div>
    <section class="main">
      <main class="article">
        <h1 class="loginTitle">회원가입</h1>
        <h2 class="subLoginTitle">브랜디/하이버의 통합회원으로 가입됩니다.</h2>
        <div class="loginContainer">
          <h3>아이디 <span class="required">(필수)</span></h3>
          <input class="loginInput" placeholder="아이디 입력" v-model="username" />
          <h3>이메일 <span class="required">(필수)</span></h3>
          <input class="loginInput" placeholder="이메일 입력" v-model="email" />
          <h3>비밀번호 <span class="required">(필수)</span></h3>
          <input class="loginInput" placeholder="비밀번호 입력" type="password" v-model="password" />
          <input class="loginInput" placeholder="비밀번호 재입력" type="password" v-model="rePassword" @keyup="checkPassword" />
          <p v-if="!isPassword">비밀번호가 옳바르지 않습니다.</p>
          <h3>휴대폰 번호 <span class="required">(필수)</span></h3>
          <div class="phonenumber">
            <input class="loginInput" placeholder="010" maxlength="3" v-model="phone1" />
            <input class="loginInput" placeholder="0000"  maxlength="4" v-model="phone2" />
            <input class="loginInput" placeholder="0000"  maxlength="4" v-model="phone3" />
            <button v-bind:class="{ phoneOk:this.checkPhone }" type="button" @click="checkPhoneHandler">인증요청</button>
          </div>

          <h3><label><CheckBox type="checkbox" v-model="allMark" /> 약관 모두 동의</label></h3>
          <div class="agreement">
            <div class="line">
              <label>
                <CheckBox type="checkbox" v-model="marks.mark1" />
                만 14세 이상입니다 <span class="required">(필수)</span>
              </label>
            </div>
            <div class="line">
              <label>
                <CheckBox type="checkbox" v-model="marks.mark2" />
                브랜디 약관 동의 <span class="required">(필수)</span>
              </label>
              <a class="more">내용보기</a>
            </div>
            <div class="line">
              <label>
                <CheckBox type="checkbox" v-model="marks.mark3" />
                개인정보수집 및 이용에 대한 안내 <span class="required">(필수)</span>
              </label>
              <a class="more">내용보기</a>
            </div>
            <div class="line">
              <label>
                <CheckBox type="checkbox" v-model="marks.mark4" />
                이벤트/마케팅 수신 동의 (선택)
              </label>
              <a class="more">내용보기</a>
            </div>
            <div class="line">
              <label>
                <CheckBox type="checkbox" v-model="marks.mark5" />
                야간 혜택 알림 수신 동의 (선택)
              </label>
              <a class="more">내용보기</a>
            </div>
          </div>

          <button type="button" class="loginBtn" :disabled="!canRegister"
            @click="onSuccess">가입하기</button>
        </div>
      </main>
    </section>
  </div>
</template>

<script>
import { SERVER_IP } from '@/config.js'
import API from '@/service/util/service-api'
import { mapMutations } from 'vuex'
import CheckBox from '@/service/Components/CheckBox'

const serviceStore = 'serviceStore'

export default {
  components: {
    CheckBox
  },
  data () {
    return {
      username: '',
      password: '',
      rePassword: '',
      isPassword: false,
      email: '',
      phone1: '',
      phone2: '',
      phone3: '',
      checkPhone: false,
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

    onSuccess () {
      console.log('회원가입')
      const data = {
        username: this.username,
        password: this.password,
        email: this.email,
        user_type_id: 1

        // phone: this.phone1 + this.phone2 + this.phone3
      }
      API.methods
        .post(`${SERVER_IP}/user/signup`, data)
        .then(() => {
          alert('가입이 완료되었습니다!')
          this.$router.push('/main')
        })
        .catch(() => {
          alert('가입이 실패하였습니다. 다시 시도해주세요.')
          this.$router.push('/main')
        })
    },

    checkPhoneHandler () {
      if (this.phone1.length === 3 && this.phone2.length === 4 && this.phone3.length === 4) {
        alert('인증되었습니다.')
        this.checkPhone = true
      } else {
        alert('핸드폰 정보를 다 입력해 주세요.')
      }
    }
  },
  mounted () {
  },
  computed: {
    checkPassword () {
      return this.password === this.rePassword
    },
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
.phoneOk {
  background-color: green;
}

span.required {
  color: red;
}
.main {
  .article {
    max-width: 1300px;
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
