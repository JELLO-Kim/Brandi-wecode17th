<template>
  <transition name="modal" appear>
    <div class="modal modal-overlay" :class="{'add-address': !isNext}" @click.self="$emit('close')">
      <div class="modal-window trans-address">
        <div class="title-box">
          <span v-if="isNext" class="title">배송지 변경</span>
          <span v-else class="title">배송지 추가</span>
          <span @click.self="$emit('close')" class="close">X</span>
        </div>

        <div class="address-box" v-bind:class="{step2: !isNext}">
          <div v-if="isNext">
            <div class="address-detail-box" v-for="address in addresses" :key="address">
              <div class="address-detail-head">
                <span>{{address.name}}</span>
                <span class="default-address" v-show="address.isDefault == 1">
                  기본배송지
                </span>
              </div>
              <div class="address-detail-body">
                <p>{{address.address}}</p>
                <p>{{address.addressDetail}}</p>
                <p>{{address.phone}}</p>
              </div>
              <div class="address-detail-footer">
                <div>
                  <button class="delete-btn" @click="delAddress(address.id)">삭제</button>
                  <!-- <button class="modify-btn">수정</button> -->
                </div>
                <div class="select-btn" @click="chooseAddress(address)">선택</div>
              </div>
            </div>

            <button class="address-add" @click="changeNext">배송지 추가</button>
          </div>

          <div v-else>
            <table class="address-input">
              <tr class="name-box">
                <th>수령인</th>
                <td><input type="text" placeholder="이름" v-model="data.name" maxlength="20"></td>
              </tr>
              <tr class="phone-box">
                <th>휴대폰</th>
                <td>
                  <input type="text" placeholder="010" v-model="phone[0]" maxlength="3">
                  <input type="text" placeholder="0000" v-model="phone[1]" maxlength="4">
                  <input type="text" placeholder="0000" v-model="phone[2]" maxlength="4">
                </td>
              </tr>
              <tr class="address-to-box">
                <th>배송지</th>
                <td>
                  <div>
                    <input type="text" v-model="data.postal" maxlength="6"><button>우편번호 찾기</button>
                  </div>
                </td>
              </tr>
              <tr class="address-to-box">
                <th></th>
                <td>
                  <input type="text" v-model="data.address">
                </td>
              </tr>
              <tr class="address-to-box">
                <th></th>
                <td>
                  <input type="text" placeholder="상세주소를 입력하세요" v-model="data.addressDetail">
                </td>
              </tr>
            </table>
          </div>
        </div>

        <div class="step2-bottom" v-if="!isNext">
          <div class="bottom-isPrivate">
            <label><CheckBox v-model="data.isDefault"></CheckBox> 기본 배송지로 저장</label>
          </div>
          <div class="bottom-btns">
            <button @click="changeNext" class="cancle-btn">취소</button>
            <button class="ok-btn" @click="save">완료</button>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script lang="cscc" scoped>
import CheckBox from '@/service/Components/CheckBox'
import SERVER from '@/config.js'
import API from '@/service/util/service-api'

export default {
  data () {
    return {
      isNext: true,
      addresses: [],
      phone: ['', '', ''],
      data: {
        name: '',
        phone: '',
        postal: '',
        address: '',
        addressDetail: '',
        isDefault: 1
      }
    }
  },
  components: {
    CheckBox
  },
  mounted () {
    this.getAddress()
  },
  methods: {
    makePayload () {
      const payload = JSON.parse(JSON.stringify(this.data))
      payload.isDefault = payload.isDefault ? 1 : 0
      payload.phone = this.phone.join('-')
      return payload
    },
    changeNext () {
      this.isNext = !this.isNext
    },
    chooseAddress (address) {
      this.$emit('choose', address)
    },
    getAddress () {
      API.methods
        .get(`${SERVER.IP}/address`)
        .then((res) => {
          // console.log(res.data.result)
          this.addresses = res.data.result.data
        })
        .catch((e) => {
          // console.log(error)
          this.$router.push('/main')
          alert(e.response.data.message)
        })
    },
    delAddress (addressId) {
      API.methods
        .delete(`${SERVER.IP}/address/delete`, {
          data: {
            addressId: addressId
          }
        })
        .then((res) => {
          this.getAddress()
        })
        .catch((e) => {
          // console.log(error)
          this.$router.push('/main')
          alert(e.response.data.message)
        })
    },
    save () {
      const payload = this.makePayload()
      API.methods
        .post(`${SERVER.IP}/address/add`, payload)
        .then((res) => {
          // console.log(res.data.result)
          this.getAddress()
          this.isNext = true
        })
        .catch((e) => {
          // console.log(error)
          this.$router.push('/main')
          alert(e.response.data.message)
        })
    }
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
.close {
  cursor: pointer;
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
.modal-window {
  height: calc(100% - 100px);
}
.add-address {
  .modal-window {
    height: 580px;
    .address-box {
      height: 330px;
      overflow-y: hidden;
    }
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
    height: calc(100% - 180px);
    overflow-y: scroll;

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
      position: absolute;
      width: calc(100% - 40px);
      bottom: 20px;
      left: 0;
      padding: 20px 0;
      margin: 0 20px;
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
