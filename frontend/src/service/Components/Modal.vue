<template>
  <transition name="modal" appear>
    <div class="modal modal-overlay" @click.self="$emit('close')">
      <div class="modal-window trans-address">
        <div class="title-box">
          <span v-if="isNext" class="title">배송지 변경</span>
          <span v-else class="title">배송지 추가</span>
          <span @click.self="$emit('close')">X</span>
        </div>

        <div class="address-box" v-bind:class="{step2: !isNext}">
          <div v-if="isNext">
            <div class="address-detail-box">
              <div class="address-detail-head">
                <span>장성준</span>
                <span class="default-address">
                  기본배송지
                </span>
              </div>
              <div class="address-detail-body">
                <p>서울 강남구 테헤란로</p>
                <p>위코드 1층</p>
                <p>010-1234-1234</p>
              </div>
              <div class="address-detail-footer">
                <div>
                  <button class="delete-btn">삭제</button>
                  <button class="modify-btn">수정</button>
                </div>
                <div class="select-btn">선택</div>
              </div>
            </div>

            <button class="address-add" @click="changeNext">배송지 추가</button>
          </div>

          <div v-else>
            <table class="address-input">
              <tr class="name-box">
                <th>수령인</th>
                <td><input type="text" placeholder="이름"></td>
              </tr>
              <tr class="phone-box">
                <th>휴대폰</th>
                <td>
                  <input type="text" placeholder="010">
                  <input type="text" placeholder="0000">
                  <input type="text" placeholder="0000">
                </td>
              </tr>
              <tr class="address-to-box">
                <th>배송지</th>
                <td>
                  <div>
                    <input type="text"><button>우편번호 찾기</button>
                  </div>
                </td>
              </tr>
              <tr class="address-to-box">
                <th></th>
                <td>
                  <input type="text">
                </td>
              </tr>
              <tr class="address-to-box">
                <th></th>
                <td>
                  <input type="text" placeholder="상세주소를 입력하세요">
                </td>
              </tr>
            </table>
          </div>
        </div>

        <div class="step2-bottom" v-if="!isNext">
          <div class="bottom-isPrivate">
            <label><CheckBox v-model="isPrivate"></CheckBox></label>
            <span>기본 배송지로 저장</span>
          </div>
          <div class="bottom-btns">
            <button @click="changeNext" class="cancle-btn">취소</button>
            <button class="ok-btn">완료</button>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script lang="cscc" scoped>
import CheckBox from '@/service/Components/CheckBox'

export default {
  data () {
    return {
      isNext: true,
      isPrivate: false
    }
  },
  methods: {
    changeNext () {
      this.isNext = !this.isNext
    }
  },
  components: {
    CheckBox
  }
}
</script>

<style lang="scss" scoped>
.modal {
  &.modal-overlay {
    display: flex;
    align-items: center;
    justify-content: center;
    position: fixed;
    z-index: 30;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
  }

  &-window {
    position: fixed;
    top:0;
    background: #fff;
    overflow: hidden;
  }

  &-content {
    padding: 10px 20px;
  }

  &-footer {
    background: #ccc;
    padding: 10px;
    text-align: right;
  }
}

.modal-enter-active, .modal-leave-active {
  transition: opacity 0.4s;

  .modal-window {
    transition: opacity 0.4s, transform 0.4s;
  }
}

.modal-leave-active {
  transition: opacity 0.6s ease 0.4s;
}

.modal-enter, .modal-leave-to {
  opacity: 0;

  .modal-window {
    opacity: 0;
    transform: translateY(-20px);
  }
}

.trans-address {
  width: 500px;
  border-top: solid 5px black;

  .title-box {
    display: flex;
    padding: 20px;
    justify-content: space-between;
    border-bottom: solid 1px rgb(228, 228, 228);
    font-size: 23px;
    font-weight: 300;

    .title {
      font-weight: 600;
    }
  }

  .address-box {
    padding: 30px;

    .address-detail-box {
      margin-bottom: 30px;
      padding: 30px;
      border: solid 1px black;
      border-radius: 4px;

      .address-detail-head {
        font-size: 25px;
        font-weight: 600;

        .default-address {
          position: relative;
          top: -3px;
          padding: 5px 15px;
          margin-left: 5px;
          border: solid 1px #9E9E9E;
          border-radius: 15px;
          font-size: 8px;
          color: #9E9E9E;
        }
      }

      .address-detail-body {
        margin: 15px 0;
        p {
          margin: 0;
          padding: 2px 0;
        }
      }

      .address-detail-footer {
        display: flex;
        justify-content: space-between;

        button {
          padding: 10px 20px;
          border: solid 1px #9E9E9E;
          border-radius: 5px;
          background-color: white;
          color: #9E9E9E;
        }

        .select-btn {
          padding: 10px 20px;
          border: 0;
          border-radius: 5px;
          background-color: black;
          color: white;
        }
      }
    }

    .address-add {
      width: 100%;
      padding: 20px 0;
      border: 0;
      border-radius: 5px;
      background-color: black;
      color: white;
      font-size: 17px;
    }
    .address-add:hover {
      cursor: pointer;
    }

    .address-input {
      font-size: 15px;

      th, td {
        padding: 5px 0;
      }
      th {
        width: 15%;
        margin-right: 20px;
        font-size: 17px;
      }
      input {
        padding: 10px;
        border: solid 1px #9E9E9E;
        border-radius: 5px;
      }

      .name-box {
        input {
          width: 100%;
        }
      }
      .phone-box input {
        width: 31%;
        margin-right: 5px;
      }
      .address-to-box {
        div {
          width: 100%;

          button {
            margin-left: 5px;
            padding: 12px 20px;
            border: 0;
            border-radius: 5px;
            background-color: black;
            color: white;
          }
          input {
            width: 66%;
          }
        }

        input {
          width: 100%;
        }
      }
    }
  }

  .step2 {
    margin-bottom: 30px;
    border-bottom: solid 1px rgb(228, 228, 228);
  }

  .step2-bottom {
    margin: 0 30px;

    .bottom-btns {
      margin-bottom: 30px;
      button {
        width: 49%;
        padding: 20px 60px;
        border: 0;
        border-radius: 5px;
        color: white;
        font-size: 17px;
      }
      .cancle-btn {
        background-color: #9E9E9E;
      }
      .ok-btn {
        background-color: black;
      }
    }
    .bottom-isPrivate {
      display: flex;
      align-content: center;
      margin-bottom: 20px;
      span {
        margin-left: 10px;
      }
    }
  }
}
</style>
