/* eslint-disable vue/no-unused-components */
<template>
  <div class="join-info">
    <Spinner v-show="isLoading" />
    <form class="join-info-container" @submit.prevent="onSubmit">
      <h1>셀러회원 가입</h1>
      <div class="line"></div>
      <img src="https://sadmin.brandi.co.kr/include/img/seller_join_top_2.png" />
      <fieldset class="join-info-text-box">
        <h2>가입 정보</h2>
        <div class="input-container">
          <i class="fa fa-user"></i>
          <div name="아이디" ref="seller_id">
            <input
              type="text"
              v-model="infoInput.account.value"
              placeholder="아이디"
              @keyup="regCheck(regs.idReg,infoInput.account)"
              :class="[infoInput.account.state ? '': 'errorInput']"
            />
          </div>
        </div>
        <div v-if="!infoInput.account.state && infoInput.account.value.length === 0" class="error">필수 입력항목입니다.</div>
        <div v-if="!infoInput.account.state && infoInput.account.value.length !== 0 && infoInput.account.value.length < 5" class="error">아이디의 최소 길이는 5글자입니다.</div>
        <div v-if="!infoInput.account.state && infoInput.account.value.length > 5" class="error">아이디는 5~20글자의 영문, 숫자, 언더바, 하이픈만 사용 가능하며 시작 문자는 영문 또는 숫자입니다.</div>
        <div class="input-container">
          <i class="fa fa-lock"></i>
          <div name="비밀번호">
            <input
              type="password"
              v-model="infoInput.password.value"
              placeholder="비밀번호"
              @keyup="regCheck(regs.idReg,infoInput.password)"
              :class="[infoInput.password.state ? '': 'errorInput']"
            />
          </div>
        </div>
        <div class="input-container">
          <i class="fa fa-check"></i>
          <div name="비밀번호확인">
            <input
              type="password"
              v-model="infoInput.password2.value"
              placeholder="비밀번호 확인"
              :class="[infoInput.password2.state ? '': 'errorInput']"
            />
          </div>
        </div>
      </fieldset>
      <fieldset class="join-info-text-box">
        <div class="title-box">
          <h2 class="h2-inline">담당자 정보</h2>
          <span class="blue-text">(*실제 샵을 운영하시는 분)</span>
        </div>
        <div class="input-container">
          <i class="fa fa-phone"></i>
          <div name="담당자 전화번호">
            <input
              type="text"
              v-model="infoInput.phone_number.value"
              placeholder="핸드폰번호"
              @keyup="regCheck(regs.phReg,infoInput.phone_number)"
              :class="[infoInput.phone_number.state ? '': 'errorInput']"
            />
          </div>
        </div>
        <div class="input-container">
          <i class="fa fa-info-circle"></i>
          <p class="blue-text">
            입점 신청 후 브랜디 담당자가 연락을 드릴 수 있으니 정확한 정보를
            기입해주세요.
          </p>
        </div>
      </fieldset>
      <fieldset class="join-info-text-box">
        <h2>셀러 정보</h2>
        <div class="radio-btn-container">
          <radio-btn
            v-for="(buttonName, idx) in radioList"
            name="radio"
            :label="idx + 1"
            :buttonName="buttonName"
            :key="idx"
            @change="change"
          />
        </div>
        <div class="input-container">
          <i class="fas fa-store"></i>
          <div name="셀러명" rules="required|korAlphaNum">
            <input
              type="text"
              v-model="infoInput.brand_name_korean.value"
              placeholder="셀러명 (상호)"
              @keyup="regCheck(regs.nameReg,infoInput.brand_name_korean)"
              :class="[infoInput.brand_name_korean.state ? '': 'errorInput']"
            />
          </div>
        </div>
        <div class="input-container">
          <i class="fa fa-font"></i>
          <div name="셀러명" rules="required|alpha_spaces">
            <input
              type="text"
              v-model="infoInput.brand_name_english.value"
              placeholder="셀러명 (영문 상호)"
              @keyup="regCheck(regs.engNameReg,infoInput.brand_name_english)"
              :class="[infoInput.brand_name_english.state ? '': 'errorInput']"
            />
          </div>
        </div>
        <div class="input-container">
          <i class="fa fa-phone"></i>
          <div name="고객센터 전화번호" rules="required|numeric|max:11">
            <input
              type="text"
              v-model="infoInput.brand_crm_number.value"
              placeholder="고객센터 전화번호"
              @keyup="regCheck(regs.telReg,infoInput.brand_crm_number)"
              :class="[infoInput.brand_crm_number.state ? '': 'errorInput']"
            />
          </div>
        </div>
      </fieldset>
      <div class="button-container">
        <bluebutton type="submit" v-on:submit="onSubmit" word="신청" />
        <div @click="alertWarn">
          <redbutton type="button" word="취소" />
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios'
import {
  idReg,
  pwReg,
  phReg,
  nameReg,
  engNameReg,
  telReg,
  urlReg
} from '@/assets/data/reg'
import ButtonBlue from '@/admin/Components/Common/ButtonBlue'
import ButtonRed from '@/admin/Components/Common/ButtonRed'
import RadioBtn from '@/admin/Components/Common/RadioBtn'
import Spinner from '@/admin/Components/Common/Spinner'
import Message from '@/admin/utils/message'
import CommonMixin from '@/admin/mixins/common-mixin'

export default {
  name: 'Signup',
  mixins: [CommonMixin],
  components: {
    bluebutton: ButtonBlue,
    redbutton: ButtonRed,
    'radio-btn': RadioBtn,
    Spinner
  },
  data () {
    return {
      regs: { idReg, pwReg, phReg, nameReg, engNameReg, telReg, urlReg },
      test: '',
      infoInput: {
        account: { value: '', state: true }, // seller_loginID
        password: { value: '', state: true }, // password
        password2: { value: '', state: true }, // password2
        phone_number: { value: '', state: true }, // phone_number
        brand_name_korean: { value: '', state: true }, // korean_name
        brand_name_english: { value: '', state: true }, // eng_name
        brand_crm_number: { value: '', state: true }, // center_number
        seller_property_id: { value: '', state: true }
      },
      radioList: [
        '쇼핑몰',
        '마켓',
        '로드샵',
        '디자이너브랜드',
        '제너럴브랜드',
        '내셔널브랜드',
        '뷰티'
      ],
      serverID: '',
      isLoading: false
    }
  },

  methods: {
    // 각 인풋창의 정규식을 이용한 체크, 인자로 해당 정규식과 data접근 경로를 써주면 된다.
    regCheck (reg, name) {
      name.state = reg.test(name.value)
    },

    // 라디오 버튼에서 v-model이 안되는 버그가 발생하여, 임시로 값 변환 하는 함수
    change (value) {
      this.infoInput.seller_property_id.value = value
    },

    alertWarn (e) {
      // console.log('hoi')
      const result = confirm('브랜디 가입을 취소하시겠습니까?')
      if (result) {
        e.preventDefault()
        this.$router.push('/')
      }
    },

    onSubmit () {
      this.isLoading = true
      const arr = Object.entries(this.infoInput)
      // filter 함수를 통해, valdiation 결과가 모두 true인지 확인합니다.
      const filterResult = arr.filter(item => {
        const result = item[1].state === false
        return result
      })

      // 위 filter 함수에서 결과가 모두 true인지 조건을 넣어 모두 true일 경우 0이므로,
      // 조건문을 이용하여 axios body에 넣을 값들을 정리합니다.
      if (filterResult.length === 0) {
        this.sendSubmit({
          account: this.infoInput.account.value,
          password: this.infoInput.password.value,
          phone_number: this.infoInput.phone_number.value,
          brand_name_korean: this.infoInput.brand_name_korean.value,
          brand_name_english: this.infoInput.brand_name_english.value,
          brand_crm_number: this.infoInput.brand_crm_number.value,
          seller_property_id: this.infoInput.seller_property_id.value
        })
      }
    },
    sendSubmit (value) {
      console.log('보내기 직전', value)
      axios
        .post(this.constants.apiDomain + '/signup', value)
        .then(res => {
          console.log('백엔드 응답', res.data)
          if (res.status === 200) {
            Message.success('회원가입을 축하합니다!')
            this.isLoading = false
            this.$router.push('/')
          }
        })
        .catch(error => {
          console.log('err', error)
          this.isLoading = true
        })
    }
  }
}
</script>

<style scoped lang="scss">
//@import "../../styles/_reset.scss";
@import "@/styles/commonD.scss";

h1 {
  margin-bottom: 20px;
  color: $darkgrey;
  font-weight: 400;
  font-size: 22px;
}

h2 {
  align-self: flex-start;
  margin-bottom: 10px;
  color: $darkgrey;
  font-weight: 400;
}

p {
  color: $darkgrey;
  font-size: 14px;
}

input[type="text"],
input[type="password"] {
  width: 360px;
  height: 35px;
  margin-bottom: 7px;
  border: 1px solid $midgrey;
  border-radius: 5px;
  background-color: white;
  text-indent: 30px;
  font-size: 13px;

  &:focus {
    outline: none;
    border: 1px solid $darkgrey;
  }

  &.invalid {
    border: 1px solid $validred;
  }
}

.validation-text {
  margin-bottom: 10px;
  color: $validred;
  font-size: 12px;
}

.join-info {
  display: flex;
  justify-content: center;
  background-color: #fafafa;
  font-family: Avenir, Helvetica, sans-serif;
  font-weight: 400;

  .line {
    width: 100%;
    height: 1px;
    margin-bottom: 20px;
    background-color: $midgrey;
  }
  .error {
    font-size: 13px;
    align-self: self-start;
    color: #a94442;
  }

  .input-container {
    position: relative;

    .fa,
    .fas {
      position: absolute;
      font-size: 14px;
      top: 10px;
      left: 10px;
      color: #e5e5e5;
    }

    .fa-phone {
      transform: rotate(100deg);
    }

    .fa-info-circle {
      font-size: 13px;
      color: $midblue;
      top: 0;
      left: 0;
    }
  }

  .join-info-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 440px;
    height: auto;
    padding: 30px;
    background-color: white;

    img {
      width: 360px;
      height: auto;
    }

    .join-info-text-box {
      display: flex;
      flex-direction: column;
      align-items: center;
      width: 360px;
      margin: 30px 0 10px 0;
      font-size: 18px;

      .blue-text {
        color: $midblue;
        font-size: 12px;
        text-indent: 15px;
        line-height: 1.3;
      }

      .title-box {
        align-self: start;
        margin-bottom: 10px;

        .h2-inline {
          display: inline;
        }
      }

      .radio-btn-container {
        display: flex;
        flex-wrap: wrap;
        width: 360px;
        margin-bottom: 20px;
        font-size: 12px;
        font-weight: 300;

        label {
          width: 100px;
        }
      }
    }
  }
  .button-container {
    display: flex;
  }

  .errorInput {
    border: 1px solid #a94442;;

    &:focus {
      border: 1px solid #a94442;;
    }
  }
}
</style>
